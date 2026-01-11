'use client';

import { useEffect, useState } from 'react';
import {
    Container, Typography, Box, Paper, Table, TableBody, TableCell,
    TableContainer, TableHead, TableRow, Chip, AppBar, Toolbar, Button
} from '@mui/material';
import { useRouter } from 'next/navigation';
import api from '../../lib/api';

interface Purchase {
    id: string;
    order_id: string;
    amount: number;
    status: 'pending' | 'completed' | 'failed';
    timestamp: string;
    voucher_identifier?: string;
}

export default function Dashboard() {
    const [purchases, setPurchases] = useState<Purchase[]>([]);
    const router = useRouter();

    const handleLogout = async () => {
        try {
            await api.post('/logout/');
            router.push('/login');
        } catch (error) {
            console.error('Logout failed', error);
            // Force redirect even if API fails (e.g. 401)
            router.push('/login');
        }
    };

    useEffect(() => {
        const fetchPurchases = async () => {
            try {
                const response = await api.get('/purchases/');
                setPurchases(response.data);
            } catch (error) {
                console.error('Failed to fetch purchases', error);
            }
        };
        fetchPurchases();
    }, []);

    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        SuperPayment Backoffice
                    </Typography>
                    <Button color="inherit" onClick={handleLogout}>Logout</Button>
                </Toolbar>
            </AppBar>

            <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
                <Typography variant="h4" gutterBottom>
                    Purchases Dashboard
                </Typography>
                <TableContainer component={Paper}>
                    <Table sx={{ minWidth: 650 }} aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell>Order ID</TableCell>
                                <TableCell align="right">Amount</TableCell>
                                <TableCell align="center">Status</TableCell>
                                <TableCell align="center">Voucher</TableCell>
                                <TableCell align="right">Timestamp</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {purchases.map((row) => (
                                <TableRow
                                    key={row.id}
                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell component="th" scope="row">
                                        {row.order_id}
                                    </TableCell>
                                    <TableCell align="right">{row.amount} €</TableCell>
                                    <TableCell align="center">
                                        <Chip
                                            label={row.status}
                                            color={row.status === 'completed' ? 'success' : row.status === 'failed' ? 'error' : 'warning'}
                                        />
                                    </TableCell>
                                    <TableCell align="center">{row.voucher_identifier || '-'}</TableCell>
                                    <TableCell align="right">{new Date(row.timestamp).toLocaleString()}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Container>
        </Box>
    );
}
