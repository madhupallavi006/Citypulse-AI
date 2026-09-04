import React, { useState } from 'react';
import { Bot, Send, Sparkles, BookOpen, User, ShieldCheck, CornerDownLeft } from 'lucide-react';
import { sendChatMessage } from '../services/api';

export default function AIAssistant() {
  const [messages, setMessages] = useState([
    {
      sender: 'assistant',
      text: 'Greetings Operator. I am **CityPulse AI Assistant**. How can I assist with traffic orchestration, signal timing, or emergency pre-emption today?',
      mode: 'RULE-BASED FALLBACK ACTIVE',
      sources: []
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeMode, setActiveMode] = useState('RULE-BASED FALLBACK ACTIVE');

  const handleSend = async (textToSend) => {
    const query = textToSend || inputMessage;
    if (!query.trim()) return;

    const userMsg = { sender: 'user', text: query };
    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInputMessage('');
    setLoading(true);

    try {
      const res = await sendChatMessage(query);
      const assistantMsg = {
        sender: 'assistant',
        text: res.reply,
        mode: res.provider_mode,
        sources: res.rag_sources || []
      };
      setMessages((prev) => [...prev, assistantMsg]);
      if (res.provider_mode) setActiveMode(res.provider_mode);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: 'assistant', text: 'Failed to reach AI Assistant server.', mode: 'ERROR', sources: [] }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const quickPrompts = [
    "What is the current traffic situation on NH16?",
    "How should we handle heavy rain in the Downtown zone?",
    "Recommend green corridor for ambulance at Vani Vihar Square."
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Bot className="w-5 h-5 text-sky-400" />
            AI Operator Assistant & RAG Knowledge Retrieval
          </h2>
          <p className="text-xs text-slate-400">Contextual traffic decision support with rule-based fallback.</p>
        </div>

        {/* Active Provider Mode Badge */}
        <span className={`px-3 py-1 text-xs font-mono rounded-full flex items-center gap-1.5 border ${
          activeMode.includes('OPENAI') ? 'bg-blue-500/10 text-blue-300 border-blue-500/30' :
          activeMode.includes('GEMINI') ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30' :
          activeMode.includes('GROQ') ? 'bg-purple-500/10 text-purple-300 border-purple-500/30' :
          'bg-amber-500/10 text-amber-300 border-amber-500/30'
        }`}>
          <ShieldCheck className="w-3.5 h-3.5" /> {activeMode}
        </span>
      </div>

      {/* Quick Prompt Pills */}
      <div className="flex flex-wrap gap-2 text-xs">
        {quickPrompts.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(prompt)}
            className="px-3 py-1.5 bg-[#131b2e] hover:bg-slate-800 border border-slate-800 text-slate-300 rounded-full transition flex items-center gap-1 font-mono text-[11px]"
          >
            <Sparkles className="w-3 h-3 text-sky-400" /> {prompt}
          </button>
        ))}
      </div>

      {/* Main Chat Stream Container */}
      <div className="bg-[#131b2e] border border-slate-800 rounded-xl p-5 h-[480px] flex flex-col justify-between space-y-4">
        {/* Messages List */}
        <div className="overflow-y-auto space-y-4 pr-2">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex items-start space-x-3 text-xs ${
                msg.sender === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {msg.sender === 'assistant' && (
                <div className="w-7 h-7 rounded-full bg-sky-500/20 text-sky-400 flex items-center justify-center shrink-0 border border-sky-500/30">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div className={`p-4 rounded-xl max-w-[85%] space-y-2 ${
                msg.sender === 'user'
                  ? 'bg-sky-600 text-white font-medium'
                  : 'bg-slate-900 border border-slate-800 text-slate-200'
              }`}>
                <div className="whitespace-pre-wrap leading-relaxed">{msg.text}</div>

                {/* RAG Sources Citations */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="pt-2 border-t border-slate-800 text-[10px] space-y-1">
                    <span className="text-slate-400 flex items-center gap-1 font-mono">
                      <BookOpen className="w-3 h-3 text-amber-400" /> RAG Knowledge Base Sources:
                    </span>
                    {msg.sources.map((s) => (
                      <div key={s.id} className="text-slate-300 font-mono bg-slate-950 p-1.5 rounded border border-slate-800/80">
                        [{s.id}] {s.title} ({s.category})
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {msg.sender === 'user' && (
                <div className="w-7 h-7 rounded-full bg-slate-800 text-slate-300 flex items-center justify-center shrink-0 border border-slate-700">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex items-center space-x-2 text-xs text-sky-400 font-mono">
              <Bot className="w-4 h-4 animate-spin" /> CityPulse AI Assistant thinking...
            </div>
          )}
        </div>

        {/* Input Bar */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center space-x-2 border-t border-slate-800 pt-3"
        >
          <input
            type="text"
            placeholder="Ask operator assistant about traffic flow, green corridors, or weather SOPs..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            className="flex-1 bg-slate-900 border border-slate-700 rounded-lg p-3 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="p-3 bg-sky-600 hover:bg-sky-500 text-white rounded-lg transition flex items-center justify-center"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
