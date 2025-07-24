"use client";

import { useEffect, useState } from "react";
import api from "../../../lib/api";

interface Experience {
  id: number;
  title: string;
  company: string;
}

interface Project {
  id: number;
  title: string;
  description: string;

}

interface ProfileData {
  experiences: Experience[];
  projects: Project[];
}

export default function ProfilePage({ params }: { params: { slug: string } }) {
  const [data, setData] = useState<ProfileData | null>(null);
  const [erro, setErro] = useState(false);

  useEffect(() => {
    api.get(`/profile/${params.slug}`)
      .then(res => setData(res.data))
      .catch(() => setErro(true));
  }, [params.slug]);

  if (erro) return <div>Erro ao carregar perfil.</div>;
  if (!data) return <div>Carregando...</div>;

  return (
    <div>
      <h1>Perfil do Usuário {params.slug}</h1>
      <h2>Experiências</h2>
      <ul>
        {data.experiences.map(exp => (
          <li key={exp.id}>
            <strong>{exp.title}</strong> em {exp.company}
          </li>
        ))}
      </ul>
      <h2>Projetos</h2>
      <ul>
        {data.projects.map(proj => (
          <li key={proj.id}>
            <strong>{proj.title}</strong>
            <p>{proj.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
