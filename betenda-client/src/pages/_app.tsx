import Loader from '@/Components/Loader/Loader'
import '@/styles/globals.css'
import { ThemeProvider } from 'next-themes'
import type { AppProps } from 'next/app'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ThemeProvider enableColorScheme={true} enableSystem={true} attribute='class'>
      <Loader />
      <Component {...pageProps} />
    </ThemeProvider>
  )
}
