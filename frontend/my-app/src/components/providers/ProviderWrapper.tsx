import React, { ReactNode } from 'react';
import NextJsThemeProvider from './ThemeProvider';

function ProviderWrapper({ children }: { children: ReactNode }) {
    return <div>
        <NextJsThemeProvider>
            {children}
        </NextJsThemeProvider>
    </div>;
}

export default ProviderWrapper;
