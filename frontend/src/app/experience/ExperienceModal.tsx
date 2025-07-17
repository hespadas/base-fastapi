"use client";

import { useState, useEffect, FormEvent, ChangeEvent } from "react";

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
  const [fields, setFields] = useState<ExperienceData>({
    title: "",
    company: "",
    description: "",
    start_date: "",
    end_date: "",
  });

  useEffect(() => {
    if (initialData) {
      setFields({
        id: initialData.id,
        title: initialData.title,
        company: initialData.company,
        description: initialData.description,
        start_date: initialData.start_date,
        end_date: initialData.end_date,
      });
    } else {
      setFields({
        title: "",
        company: "",
        description: "",
        start_date: "",
        end_date: "",
      });
    }
  }, [initialData]);

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFields(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit(fields);
  };

  const isEditing = Boolean(initialData);

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
        <h2 className="text-xl font-semibold mb-4 text-gray-900">
          {isEditing ? "Edit Experience" : "Save Experience"}
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">

          <div className="flex flex-col">
            <label htmlFor="title" className="mb-1 text-sm font-medium text-gray-800">
              Title
            </label>
            <input
              id="title"
              name="title"
              type="text"
              placeholder="Título"
              value={fields.title}
              onChange={handleChange}
              className="w-full p-2 border rounded text-gray-900 placeholder-gray-500 border-gray-400"
              required
            />
          </div>

          <div className="flex flex-col">
            <label htmlFor="company" className="mb-1 text-sm font-medium text-gray-800">
              Company
            </label>
            <input
              id="company"
              name="company"
              type="text"
              placeholder="Company"
              value={fields.company}
              onChange={handleChange}
              className="w-full p-2 border rounded text-gray-900 placeholder-gray-500 border-gray-400"
              required
            />
          </div>

          <div className="flex flex-col">
            <label htmlFor="description" className="mb-1 text-sm font-medium text-gray-800">
              Description
            </label>
            <textarea
              id="description"
              name="description"
              placeholder="Description"
              value={fields.description}
              onChange={handleChange}
              className="w-full p-2 border rounded text-gray-900 placeholder-gray-500 border-gray-400"
              required
            />
          </div>

          <div className="flex flex-col">
            <label htmlFor="startDate" className="mb-1 text-sm font-medium text-gray-800">
              Start Date
            </label>
            <input
              id="startDate"
              name="start_date"
              type="date"
              value={fields.start_date}
              onChange={handleChange}
              className="w-full p-2 border rounded text-gray-900 border-gray-400"
              required
            />
          </div>

          <div className="flex flex-col">
            <label htmlFor="endDate" className="mb-1 text-sm font-medium text-gray-800">
              End Date
            </label>
            <input
              id="endDate"
              name="end_date"
              type="date"
              value={fields.end_date}
              onChange={handleChange}
              className="w-full p-2 border rounded text-gray-900 border-gray-400"
            />
          </div>

          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white font-medium rounded hover:bg-blue-700 transition"
            >
              {isEditing ? "Save" : "Add"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
