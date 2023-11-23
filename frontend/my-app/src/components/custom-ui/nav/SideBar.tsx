'use client';
import ThemeSwitchButton from '@/components/ui/theme-switch-button';
import { classNames } from '@/lib/utils';
import {
    BrainCircuitIcon,
    HomeIcon,
    LucideIcon,
    NetworkIcon,
} from 'lucide-react';
import Link from 'next/link';
import React, { useState } from 'react';

interface SideBarNavType {
    name: string;
    href: string;
    icon: LucideIcon;
    current: boolean;
}

function SideBar() {
    const [sideBarNav, setSideBarNav] = useState<SideBarNavType[]>([
        { name: 'Dashbard', href: '/', icon: HomeIcon, current: true },
    ]);

    const handleLinkClick = (name: string) => {
        const updatedNav = sideBarNav.map((item) => ({
            ...item,
            current: item.name === name,
        }));
        setSideBarNav(updatedNav);
    };

    return (
        <div className='hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-64 lg:flex-col h-full'>
            <div className='flex grow flex-col gap-y-5 overflow-y-auto border-r border-secondary px-6 py-3 bg-secondary justify-between'>
                <div className='flex grow flex-col gap-y-5 overflow-y-auto'>
                    <div className='flex h-16 shrink-0 items-center justify-center'>
                        <h1 className='text-secondary-foreground w-auto font-bold text-3xl'>
                            Chess AI
                        </h1>
                    </div>
                    <nav className='flex flex-1 flex-col'>
                        <ul
                            role='list'
                            className='flex flex-1 flex-col gap-y-5'
                        >
                            {sideBarNav.map((item) => (
                                <li key={item.name}>
                                    <Link
                                        href={item.href}
                                        className={classNames(
                                            item.current
                                                ? 'bg-secondary-200'
                                                : 'bg-secondary hover:bg-secondary-200',
                                            'text-secondary-foreground p-3 rounded-lg flex flex-row group gap-x-3 font-bold',
                                        )}
                                        onClick={() =>
                                            handleLinkClick(item.name)
                                        }
                                    >
                                        <item.icon className='h-6 w-6 shrink-0' />
                                        {item.name}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </nav>
                </div>
                <div className='flex mb-5 justify-center'>
                    <ThemeSwitchButton />
                </div>
            </div>
        </div>
    );
}

export default SideBar;
