"use client";

import {useEffect, useState} from "react";
import {useAuth} from "@/hooks/useAuth";
import api from '../../lib/api';
import CreateExperienceModal from "./CreateExperienceModal";

export default function Profile() {

    const [modalOpen, setModalOpen] = useState(false);
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
        <section className="flex flex-col items-center justify-center min-h-screen bg-gray-100 px-4">
            <h1 className="text-4xl font-bold mb-6 text-gray-900">Experiences</h1>
            <div className="w-full max-w-2xl space-y-6">
                {experiences.length > 0 ? (
                    experiences.map((experience) => (
                        <div key={experience.id} className="p-6 bg-white rounded-lg shadow-md border border-gray-200">
                            <h2 className="text-xl font-semibold text-gray-800">{experience.title}</h2>
                            <p className="text-gray-700 font-medium mt-1">Company: {experience.company}</p>
                            <p className="text-gray-800 my-2">{experience.description}</p>
                            <div className="flex flex-col mt-3 text-sm">
                                <p className="text-gray-600">Start date: <span className="font-medium">{experience.start_date}</span></p>
                                <p className="text-gray-600">End date: <span className="font-medium">{experience.end_date}</span></p>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className="text-gray-700 text-center py-8">No experiences found.</p>
                )}
            </div>
            <button
                onClick={() => setModalOpen(true)}
                className="mt-6 px-6 py-2 bg-blue-600 text-white font-medium rounded-md shadow hover:bg-blue-700 transition-colors"
            >
                Add Experience
            </button>
            {modalOpen && (
                <CreateExperienceModal
                    onClose={() => setModalOpen(false)}
                    onCreate={(data) => {
                        api.post('/experiences', data)
                            .then(response => {
                                setExperiences([...experiences, response.data]);
                            })
                    }}
                />
            )}
        </section>
    )
}