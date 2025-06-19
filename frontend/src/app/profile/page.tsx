"use client";

import {useEffect, useState} from "react";

export default function Profile() {

    const [user, setUser] = useState(null);
    const [experiences, setExperiences] = useState([]);

    useEffect(() => {
            fetch("/api/experiences")
                .then(response => response.json())
                .then(data => {
                    setExperiences(data);
                })
                .catch(error => {
                    console.error("Error fetching experiences:", error);
                });
            fetch("/api/user")
                .then(response => response.json())
                .then(data => {
                    setUser(data);
                })
                .catch(error => {
                    console.error("Error fetching user:", error);
                });
        }
        , []);

    return (
        <section className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-4">
            <h1 className="text-4xl font-bold mb-6">Experiences</h1>
            <div className="w-full max-w-2xl space-y-6">
                {experiences.map((experience) => (
                    <div key={experience.id} className="bg-white shadow-md rounded-lg p-6 mb-4">
                        <h2 className="text-2xl font-semibold mb-2">{experience.title}</h2>
                        <p className="text-gray-700 mb-4">{experience.description}</p>
                        <p className="text-sm text-gray-500">Created by: {user?.username || "Loading..."}</p>
                    </div>
                ))}
                {experiences.length === 0 && (
                    <p className="text-gray-500">No experiences found.</p>
                )}
            </div>
        </section>
    )

}
