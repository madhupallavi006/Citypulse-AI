import React, { useState } from 'react';
import { MessageSquareCode, Send, Bot, User, BookOpen, Cpu } from 'lucide-react';
import { sendChatMessage } from '../services/api';

export default function AIAssistant() {
  const [messages, setMessages] = useState([
    {
      sender: 'assistant',
      text: 'Hello Operator. I am CityPulse AI Assistant. Ask me about live traffic conditions, predicted congestion risks, emergency green corridors, or traffic management strategies.',
      sources: ['CityPulse Telemetry Stream', 'RAG ChromaDB Knowledge Index'],
      fallback: true
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userQuery = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { sender: 'user', text: userQuery }]);
    setLoading(true);

    try {
      const data = await sendChatMessage(userQuery);
      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: data.response,
          sources: data.sources || [],
          fallback: data.fallback_mode
        }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: 'assistant', text: 'Error contacting AI assistant backend service.', sources: [] }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <MessageSquareCode className="w-5 h-5 text-sky-400" />
          CityPulse Operator AI Assistant & RAG Knowledge Base
        </h2>
        <p className="text-xs text-slate-400">
          LLM-driven operator assistant grounded in real-time telemetry, ML forecasts, and traffic management docs.
        </p>
      </div>

      <div className="bg-[#131b2e] border border-slate-800 rounded-xl h-[550px] flex flex-col overflow-hidden">
        {/* Chat Message History */}
        <div className="flex-1 p-4 overflow-y-auto space-y-4">
          {messages.map((m, idx) => (
            <div key={idx} className={`flex gap-3 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              {m.sender === 'assistant' && (
                <div className="w-8 h-8 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center shrink-0">
                  <Bot className="w-4 h-4 text-sky-400" />
                </div>
              )}

              <div className={`max-w-xl rounded-xl p-3 text-xs space-y-2 ${
                m.sender === 'user' ? 'bg-sky-600 text-white font-medium' : 'bg-slate-900 border border-slate-800 text-slate-200'
              }`}>
                <p className="leading-relaxed whitespace-pre-wrap">{m.text}</p>

                {m.sources && m.sources.length > 0 && (
                  <div className="pt-2 border-t border-slate-800 text-[10px] font-mono text-slate-400 flex items-center gap-1.5 flex-wrap">
                    <BookOpen className="w-3 h-3 text-sky-400" />
                    <span>Grounding Sources:</span>
                    {m.sources.map((src, i) => (
                      <span key={i} className="px-1.5 py-0.5 bg-slate-800 text-slate-300 rounded border border-slate-700">
                        {src}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {m.sender === 'user' && (
                <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0">
                  <User className="w-4 h-4 text-slate-300" />
                </div>
              )}
            </div>
          ))}
          {loading && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center animate-pulse">
                <Bot className="w-4 h-4 text-sky-400" />
              </div>
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-xs text-slate-400 font-mono flex items-center space-x-2">
                <Cpu className="w-3.5 h-3.5 animate-spin text-sky-400" />
                <span>Synthesizing live telemetry & RAG knowledge base...</span>
              </div>
            </div>
          )}
        </div>

        {/* Chat Input Bar */}
        <form onSubmit={handleSend} className="p-3 bg-slate-900 border-t border-slate-800 flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask AI Assistant e.g., 'Which roads are expected to become congested?'..."
            className="flex-1 bg-[#131b2e] border border-slate-700 rounded-lg px-4 py-2 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 transition disabled:opacity-50"
          >
            <Send className="w-3.5 h-3.5" />
            <span>Send</span>
          </button>
        </form>
      </div>
    </div>
  );
}
