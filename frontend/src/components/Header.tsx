"use client"
import Link from "next/link"
import { useAuth } from "@/hooks/useAuth"

export default function Header() {
  const { user, logout } = useAuth()

  return (
    <header style={{ display: "flex", gap: 16 }}>
      <Link href="/">Home</Link>
      {user ? (
        <>
          <span>Hello, {user.username}</span>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <>
          <Link href="/login">Login</Link>
          <Link href="/signup">Signup</Link>
        </>
      )}
    </header>
  )
}
