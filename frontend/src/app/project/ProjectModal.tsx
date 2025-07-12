"use client";

import { useEffect, useState } from "react";

export interface ProjectData {
    id?: number;
    title: string;
    description: string;
    github_url: string;
    project_url: string;
}

interface CreateEditProjectModalProps {
    onClose: () => void;
    onSubmit: (data: ProjectData) => void;
    initialData?: ProjectData;
}

export default function CreateEditProjectModal({
    onClose,
    onSubmit,
    initialData,
}: CreateEditProjectModalProps) {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [githubUrl, setGithubUrl] = useState("");
    const [projectUrl, setProjectUrl] = useState("");

    useEffect(() => {
        if (initialData) {
            setTitle(initialData.title);
            setDescription(initialData.description);
            setGithubUrl(initialData.github_url);
            setProjectUrl(initialData.project_url);
        }
    }
    , [initialData]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const payload: ProjectData = {
            ...(initialData && { id: initialData.id }),
            title,
            description,
            github_url: githubUrl,
            project_url: projectUrl,
        };
        onSubmit(payload);
    }

    const isEditing = Boolean(initialData);

    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
                <h2 className="text-xl font-semibold mb-4 text-gray-900">
                    {isEditing ? "Editar Projeto" : "Adicionar Projeto"}
                </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Título</label>
                        <input
                            type="text"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Descrição</label>
                        <textarea
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            required
                            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">URL do GitHub</label>
                        <input
                            type="str"
                            value={githubUrl}
                            onChange={(e) => setGithubUrl(e.target.value)}
                            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">URL do Projeto</label>
                        <input
                            type="str"
                            value={projectUrl}
                            onChange={(e) => setProjectUrl(e.target.value)}
                            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                        />
                    </div>
                    <div className="flex justify-end space-x-2">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                        >
                            {isEditing ? "Salvar" : "Adicionar"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}


