import { useState, FormEvent } from "react";

interface CreateExperienceModalProps {
    onClose: () => void;
    onCreate: (data: { title: string; company: string; description: string; start_date: string; end_date: string }) => void;
}

export default function CreateExperienceModal({ onClose, onCreate }: CreateExperienceModalProps) {
    const [title, setTitle] = useState("");
    const [company, setCompany] = useState("");
    const [description, setDescription] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        onCreate({ title, company, description, start_date: startDate, end_date: endDate });
        onClose();
    };

    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
                <h2 className="text-xl font-semibold mb-4 text-gray-900">Adicionar Experiência</h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="flex flex-col">
                        <label htmlFor="title" className="mb-1 text-sm font-medium text-gray-800">Título</label>
                        <input
                            id="title"
                            type="text"
                            placeholder="Título"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            className="w-full p-2 border rounded text-gray-900 placeholder-gray-500 border-gray-400"
                            required
                        />
                    </div>

                    <div className="flex flex-col">
                        <label htmlFor="company" className="mb-1 text-sm font-medium text-gray-800">Empresa</label>
                        <input
                            id="company"
                            type="text"
                            placeholder="Empresa"
                            value={company}
                            onChange={(e) => setCompany(e.target.value)}
                            className="w-full p-2 border rounded text-gray-900 placeholder-gray-500 border-gray-400"
                            required
                        />
                    </div>

                    <div className="flex flex-col">
                        <label htmlFor="description" className="mb-1 text-sm font-medium text-gray-800">Descrição</label>
                        <textarea
                            id="description"
                            placeholder="Descrição"
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            className="w-full p-2 border rounded text-gray-900 placeholder-gray-500 border-gray-400"
                            required
                        />
                    </div>

                    <div className="flex flex-col">
                        <label htmlFor="startDate" className="mb-1 text-sm font-medium text-gray-800">Data de Início</label>
                        <input
                            id="startDate"
                            type="date"
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                            className="w-full p-2 border rounded text-gray-900 border-gray-400"
                            required
                        />
                    </div>

                    <div className="flex flex-col">
                        <label htmlFor="endDate" className="mb-1 text-sm font-medium text-gray-800">Data de Término</label>
                        <input
                            id="endDate"
                            type="date"
                            value={endDate}
                            onChange={(e) => setEndDate(e.target.value)}
                            className="w-full p-2 border rounded text-gray-900 border-gray-400"
                        />
                    </div>

                    <div className="flex justify-end space-x-2">
                        <button type="button" onClick={onClose} className="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 transition">Cancelar</button>
                        <button type="submit" className="px-4 py-2 bg-blue-600 text-white font-medium rounded hover:bg-blue-700 transition">Adicionar</button>
                    </div>
                </form>
            </div>
        </div>
    );
}