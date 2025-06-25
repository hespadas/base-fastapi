"use client";

import {useEffect, useState} from "react";
import {useAuth} from "@/hooks/useAuth";
import api from '../../lib/api';

export default function Profile() {

    const {user} = useAuth()
    const [experiences, setExperiences] = useState([]);

    useEffect(() => {
        async function fetchExperiences() {
            try {
                const response = await api.get('/experiences');
                setExperiences(response.data);
            } catch (error) {
                console.error("Error fetching experiences:", error);
            }
        }

        fetchExperiences();
    }, []);

    return (
        <section className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-4">
            <h1 className="text-4xl font-bold mb-6">Experiences</h1>
            <div className="w-full max-w-2xl space-y-6">
                {experiences.length > 0 ? (
                    experiences.map((experience) => (
                        <div key={experience.id} className="p-4 bg-white rounded-lg shadow-md">
                            <h2 className="text-xl font-semibold">{experience.title}</h2>
                            <p className="text-gray-600">Company: {experience.company}</p>
                            <p className="text-gray-700">{experience.description}</p>
                            <p className="text-sm text-gray-500">Start at:{experience.start_date}</p>
                            <p className="text-sm text-gray-500">End at:{experience.end_date}</p>
                        </div>
                    ))
                ) : (
                    <p className="text-gray-500">No experiences found.</p>
                )}
            </div>
        </section>
    )
}
