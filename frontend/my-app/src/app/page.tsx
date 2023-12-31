import ChessBoard from '@/components/chess/ChessBoard';
import ChessBoardView from '@/components/chess/ChessBoardView';

export default async function Home() {
    return (
        <main className='py-10 lg:pl-64 w-full'>
            <div className='px-10'>
                <div className='flex flex-col justify-center gap-y-10'>
                    <div className='items-center'>
                        <h1 className='text-2xl font-semibold text-center'>
                            Dashboard
                        </h1>
                    </div>
                    <div className='p-1 flex justify-center mt-6'>
                        <ChessBoardView />
                    </div>
                </div>
            </div>
        </main>
    );
}
