'use client';
import { GET } from '@/lib/apiClient';
import { components } from '@/lib/openapi';
import React, { useEffect, useState } from 'react';
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '../ui/select';
import ChessBoard from './ChessBoard';

function ChessBoardView() {
    const [gameList, setGameList] = useState<
        components['schemas']['Game'][] | undefined
    >([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<
        components['schemas']['HTTPValidationError'] | undefined
    >();
    const [game, setGame] = useState('');

    const getGameList = async () => {
        setIsLoading(true);
        const { data, error } = await GET('/game/games');
        if (error) {
            console.log(error);
            setIsLoading(false);
            setError(error);
            return;
        }

        setGameList(data);
        setIsLoading(false);
    };

    useEffect(() => {
        getGameList();
    }, []);

    return (
        <div className='flex flex-col justify-center'>
            {isLoading && <p>Loading...</p>}
            {error && <>{error.detail?.map((detail) => <p>{detail.msg}</p>)}</>}
            {gameList && (
                <Select onValueChange={(value) => setGame(value)}>
                    <SelectTrigger className='p-1 px-2'>
                        <SelectValue placeholder='Select Game' />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectGroup>
                            {gameList.map((game) => (
                                <SelectItem
                                    key={game.id}
                                    value={game.id.toString()}
                                >
                                    {game.id}
                                </SelectItem>
                            ))}
                        </SelectGroup>
                    </SelectContent>
                </Select>
            )}
            {game === '' ? (
                <p>No game selected</p>
            ) : (
                <div className='p-1 flex justify-center mt-6'>
                    <ChessBoard id={game} />
                </div>
            )}
        </div>
    );
}

export default ChessBoardView;
