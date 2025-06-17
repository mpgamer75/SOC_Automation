import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Altice File Comparator',
  description: 'Compara archivos CSV, Excel y XLS de manera inteligente',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  )
}
