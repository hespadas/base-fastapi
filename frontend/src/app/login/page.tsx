"use client";

import {FormEvent, useState} from "react";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        setError("");

        try {
            const response = await fetch(`${apiUrl}/api/access_token`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: formData,
            });
            if (!response.ok) {
                const errorData = await response.json();
                setError(errorData.message || "An error occurred during login.");
                return;
            } else {
                const data = await response.json();
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("refresh_token", data.refresh_token);
                setSuccess(true);
                window.location.href = "/";
            }
        } catch (err) {
            setError("An unexpected error occurred. Please try again later.");
            return;
        }
    }

    return (
        <section>
            <div>
                <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-4">
                    <h1 className="text-4xl font-bold mb-6">Login</h1>
                    <form className="w-full max-w-md space-y-6" onSubmit={handleSubmit}>
                        <div>
                            <label htmlFor="username" className="block text-sm font-medium text-gray-700">Username</label>
                            <input
                                type="username"
                                id="username"
                                required
                                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </div>
                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
                            <input
                                type="password"
                                id="password"
                                required
                                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm text-gray-900"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                        {error && (
                            <p className="text-red-600">{error}</p>
                        )}
                        {success && (
                            <p className="text-green-600">Login successful! Redirecting...</p>
                        )}
                        <button
                            type="submit"
                            className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                        >
                            Login
                        </button>
                    </form>
                </div>
            </div>
        </section>
    )
}