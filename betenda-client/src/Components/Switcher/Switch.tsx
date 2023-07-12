import { useTheme } from 'next-themes'
import { useEffect, useState } from "react";
import { FiSun, FiMoon } from 'react-icons/fi'

const Switcher = () => {
    const { systemTheme, theme, setTheme } = useTheme();
    const [mounted, setMounted] = useState(false);


    useEffect(() => {
        setMounted(true);
    }, []);

    if (!mounted) return null;
    const currentTheme = theme === 'system' ? systemTheme : theme;

    const toggleDarkMode = () => {
        if (mounted) setTheme(currentTheme === 'dark' ? 'light' : 'dark')
    };

    return (
        <>
            <button onClick={toggleDarkMode} className="rounded-full w-10 h-10 bor-lyr flex items-center justify-center">
                {currentTheme === 'dark' ? <FiSun size="22" /> : <FiMoon size="22" />}
            </button>
        </>
    );
}

export default Switcher