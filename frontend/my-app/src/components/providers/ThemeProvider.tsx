'use client';
import { ThemeProvider } from 'next-themes';
import React, { ReactNode } from 'react';

function NextJsThemeProvider({ children }: { children: ReactNode }) {
    return (
        <ThemeProvider
            attribute='class'
            defaultTheme='system'
            enableSystem
            disableTransitionOnChange
        >
            {children}
        </ThemeProvider>
    );
}

export default NextJsThemeProvider;
