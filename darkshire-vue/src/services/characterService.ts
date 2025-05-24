import axios from 'axios';

export interface Character {
  id?: number;
  name: string;
  class: string;
  spec: string;
  level: number;
  professions: string[];
  photo_url?: string;
}

const API = axios.create({
  baseURL: 'https://shadowheartlover.biz/api/characters'
});

export const listCharacters = async (): Promise<Character[]> => {
  const { data } = await API.get<Character[]>('');
  return data;
};

// For JSON‑only (no photo)
export const addCharacter = async (char: Character): Promise<Character> => {
  const { data } = await API.post<Character>('', char);
  return data;
};

// For multipart/form-data (with optional photo)
export const uploadCharacter = async (formData: FormData): Promise<Character> => {
  const { data } = await API.post<Character>('', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return data;
};

export const getCharacter = async (id: number): Promise<Character> => {
  const { data } = await API.get<Character>(`/${id}`);
  return data;
};

export const updateCharacter = async (
  id: number,
  fields: Partial<Pick<Character, 'level' | 'professions'>>
): Promise<Character> => {
  const { data } = await API.patch<Character>(`/${id}`, {
    // if professions is an array, leave it; Flask handler will stringify
    ...fields
  });
  return data;
};