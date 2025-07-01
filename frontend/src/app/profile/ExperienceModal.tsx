"use client";

import { useState, useEffect, FormEvent } from "react";

export interface ExperienceData {
  id?: number;
  title: string;
  company: string;
  description: string;
  start_date: string;
  end_date: string;
}

interface CreateEditExperienceModalProps {
  onClose: () => void;
  onSubmit: (data: ExperienceData) => void;
  initialData?: ExperienceData;
}

export default function CreateEditExperienceModal({
  onClose,
  onSubmit,
  initialData,
}: CreateEditExperienceModalProps) {
  const [title, setTitle] = useState("");
  const [company, setCompany] = useState("");
  const [description, setDescription] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title);
      setCompany(initialData.company);
      setDescription(initialData.description);
      setStartDate(initialData.start_date);
      setEndDate(initialData.end_date);
    }
  }, [initialData]);

  const handleSubmit = (e: FormEvent) => {
  e.preventDefault();
  const payload: ExperienceData = {
    ...(initialData && { id: initialData.id }),
    title,
    company,
    description,
    start_date: startDate,
    end_date: endDate,
  };
  onSubmit(payload);
};

  const isEditing = Boolean(initialData);

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
        <h2 className="text-xl font-semibold mb-4 text-gray-900">
          {isEditing ? "Editar Experiência" : "Adicionar Experiência"}
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">

          <div className="flex flex-col">
            <label htmlFor="title" className="mb-1 text-sm font-medium text-gray-800">
              Título
            </label>
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
            <label htmlFor="company" className="mb-1 text-sm font-medium text-gray-800">
              Empresa
            </label>
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
            <label htmlFor="description" className="mb-1 text-sm font-medium text-gray-800">
              Descrição
            </label>
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
            <label htmlFor="startDate" className="mb-1 text-sm font-medium text-gray-800">
              Data de Início
            </label>
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
            <label htmlFor="endDate" className="mb-1 text-sm font-medium text-gray-800">
              Data de Término
            </label>
            <input
              id="endDate"
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-full p-2 border rounded text-gray-900 border-gray-400"
            />
          </div>

          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 transition"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white font-medium rounded hover:bg-blue-700 transition"
            >
              {isEditing ? "Salvar" : "Adicionar"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
