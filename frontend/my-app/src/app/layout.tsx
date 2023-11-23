import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import ProviderWrapper from '@/components/providers/ProviderWrapper';
import SideBar from '@/components/custom-ui/nav/SideBar';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'Chess AI',
    description: 'The landding page for ChessAI',
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang='en' className='h-full'>
            <body className={inter.className + 'h-full'}>
                <ProviderWrapper>
                    <div className='flex flex-row'>
                        <SideBar />
                        {children}
                    </div>
                </ProviderWrapper>
            </body>
        </html>
    );
}
