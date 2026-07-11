import { useState } from 'react';
import UploadZone from './components/UploadZone';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [docText, setDocText] = useState<string>(""); 
  const [analysis, setAnalysis] = useState<string>(""); 
  const [query, setQuery] = useState<string>(""); 
  const [status, setStatus] = useState<'idle' | 'loading' | 'success'>('idle');

  const handleUpload = async (file: File) => {
    setFile(file);
    setStatus('loading');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/file/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error("Ошибка загрузки");
      const result = await response.json();
      setDocText(result.message || "Файл успешно обработан");
      setStatus('success');
    } catch (err) {
      alert("Ошибка при загрузке");
      setStatus('idle');
      setFile(null);
    }
  };

  const askAI = async () => {
    if (!query.trim()) return;

    try {
      const params = new URLSearchParams({ query: query });
      const response = await fetch(`http://localhost:8000/main/ask?${params.toString()}`, {
        method: 'POST',
      });
      
      if (!response.ok) throw new Error("Ошибка при запросе к ИИ");
      const data = await response.json();
      setAnalysis(data.answer || data || "Нет ответа");
    } catch (err) {
      alert("Не удалось получить анализ");
    }
  };

  return (
    <div className="min-h-screen bg-white text-gray-900 p-8 max-w-3xl mx-auto font-sans">
      <h1 className="text-2xl font-light mb-8">Brainbook</h1>

      {/* Секция загрузки */}
      <section className="mb-10">
        <h2 className="text-sm font-light uppercase tracking-widest text-gray-500 mb-4">Материал</h2>
        {!file ? (
          <UploadZone onUpload={handleUpload} />
        ) : (
          <div className="p-6 border border-gray-200 rounded-sm">
            <pre className="text-sm font-light text-gray-600 whitespace-pre-wrap">{docText}</pre>
          </div>
        )}
      </section>

      {/* Секция анализа */}
      <section>
        <h2 className="text-sm font-light uppercase tracking-widest text-gray-500 mb-4">Анализ</h2>
        <div className="space-y-4">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Введите вопрос..."
            className="w-full p-4 border border-gray-200 rounded-sm focus:outline-none focus:border-black transition-colors font-light text-sm"
          />
          
          <div className="p-6 bg-gray-50 border border-gray-100 min-h-[100px]">
            <p className="text-sm font-light text-gray-700 leading-relaxed">{analysis || "Здесь будет ответ..."}</p>
          </div>
          
          <button 
            onClick={askAI}
            disabled={status !== 'success'}
            className="w-full py-3 bg-black text-white text-sm font-light tracking-wide hover:bg-gray-800 transition-all disabled:bg-gray-200 disabled:text-gray-400"
          >
            Спросить у AI
          </button>
        </div>
      </section>
    </div>
  );
}

export default App;