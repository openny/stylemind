import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

// API URL 정의 (백엔드 주소에 맞게 수정)
const API_URL = 'http://localhost:8080/api';

function App() {
  const [urls, setUrls] = useState(['']);
  const [analysis, setAnalysis] = useState<any>(null);
  const [topic, setTopic] = useState(''); // 누락된 topic 상태 추가
  const [statusText, setStatusText] = useState(''); // 누락된 statusText 상태 추가
  const [image, setImage] = useState<File | null>(null);
  const [generatedPost, setGeneratedPost] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleUrlChange = (index: number, value: string) => {
    const newUrls = [...urls];
    newUrls[index] = value;
    setUrls(newUrls);
  };

  const addUrlField = () => setUrls([...urls, '']);

  const handleAnalyze = async () => {
    setLoading(true);
    setStatusText('블로그 어투를 분석 중입니다...');
    try {
      const validUrls = urls.filter(u => u.trim() !== '');
      if (validUrls.length === 0) return alert('URL을 입력해주세요.');

      const res = await axios.post(`${API_URL}/analyze-style`, { urls: validUrls });
      setAnalysis(res.data.result);
    } catch (e: any) {
      alert('분석 실패: ' + e.message);
    }
    setLoading(false);
  };

  const handleGenerate = async () => {
    if (!analysis || !image || !topic) return alert("모든 필드를 입력해주세요.");
    setLoading(true);
    setStatusText('이미지를 분석하고 글을 작성 중입니다... (약 1-2분 소요)');

    const formData = new FormData();
    formData.append('topic', topic);
    formData.append('style_prompt', analysis.style_prompt);
    formData.append('image', image);

    try {
      const res = await axios.post(`${API_URL}/generate-post`, formData);
      setGeneratedPost(res.data);
    } catch (e: any) {
      alert('생성 실패: ' + e.message);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">AI 블로그 에이전트</h1>
          <p className="mt-2 text-gray-600">내 어투를 학습하여 이미지 기반 블로그 글을 자동으로 작성합니다.</p>
        </div>

        {/* 1. 스타일 분석 섹션 */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">1. 블로그 스타일 분석</h2>
          <div className="space-y-3">
            {urls.map((url, idx) => (
              <input
                key={idx}
                type="text"
                value={url}
                onChange={(e) => handleUrlChange(idx, e.target.value)}
                placeholder="네이버/티스토리 블로그 포스트 URL 입력"
                className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
              />
            ))}
            <div className="flex gap-2">
              <button onClick={addUrlField} className="text-blue-600 text-sm hover:underline">+ URL 추가</button>
            </div>
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="w-full mt-4 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
            >
              스타일 분석 시작
            </button>
          </div>

          {analysis && (
            <div className="mt-6 p-4 bg-green-50 rounded border border-green-200">
              <h3 className="font-bold text-green-800">분석 완료!</h3>
              <ul className="mt-2 text-sm text-green-700 list-disc list-inside">
                <li>평균 문장 길이: {analysis.avg_length}자</li>
                <li>주요 말투: {analysis.is_polite? "존댓말(해요체)" : "반말(해체)"}</li>
                <li>자주 쓰는 어미: {analysis.top_endings.join(", ")}</li>
              </ul>
            </div>
          )}
        </div>

        {/* 2. 글 생성 섹션 */}
        {analysis && (
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">2. 새 글 작성</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">주제</label>
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  className="mt-1 w-full p-2 border rounded"
                  placeholder="예: 주말 한강 피크닉"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">이미지 업로드</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => setImage(e.target.files ? e.target.files[0] : null)}
                  className="mt-1 w-full"
                />
              </div>
              <button
                onClick={handleGenerate}
                disabled={loading}
                className="w-full bg-indigo-600 text-white py-3 rounded text-lg font-semibold hover:bg-indigo-700 disabled:bg-gray-400"
              >
                {loading? statusText : "블로그 글 생성하기"}
              </button>
            </div>
          </div>
        )}

        {/* 3. 결과 출력 */}
        {generatedPost && (
          <div className="bg-white p-8 rounded-lg shadow ring-1 ring-gray-200">
            <h2 className="text-2xl font-bold mb-6">{topic}</h2>
            <div className="prose max-w-none">
              <ReactMarkdown>{generatedPost.content}</ReactMarkdown>
            </div>
            <div className="mt-8 pt-4 border-t text-sm text-gray-500">
              <p>💡 AI가 분석한 이미지 내용: {generatedPost.image_desc}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;