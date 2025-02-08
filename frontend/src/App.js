import React, { useState, useRef } from 'react';
import { FileText, Copy, Share2, Upload, Link, RefreshCw } from 'lucide-react';
import axios from 'axios';

const App = () => {
  const [text, setText] = useState('');
  const [url, setUrl] = useState('');
  const [summaryRatio, setSummaryRatio] = useState('brief');
  const [summary, setSummary] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [copySuccess, setCopySuccess] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [summaryHistory, setSummaryHistory] = useState([]);
  const fileInputRef = useRef(null);

  const handleSummarize = async () => {
    setIsProcessing(true);
    try {
      const response = await axios.post('http://localhost:5001/api/summarize', {
        text,
        url: url || null,
        type: summaryRatio
      });
      const newSummary = {
        id: Date.now(),
        content: response.data.summary,
        type: summaryRatio,
        timestamp: new Date().toLocaleString()
      };
      setSummary(newSummary.content);
      setSummaryHistory(prev => [newSummary, ...prev].slice(0, 5));
    } catch (error) {
      console.error('Error details:', error.response?.data);
      setSummary('Unable to generate summary. Please try again.');
    }
    setIsProcessing(false);
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', summaryRatio);

    setIsProcessing(true);
    try {
      const response = await axios.post('http://localhost:5001/api/summarize/file', 
        formData,
        {
          headers: { 
            'Content-Type': 'multipart/form-data'
          },
          params: { type: summaryRatio }
        }
      );
      const newSummary = {
        id: Date.now(),
        content: response.data.summary,
        type: summaryRatio,
        timestamp: new Date().toLocaleString()
      };
      setSummary(newSummary.content);
      setSummaryHistory(prev => [newSummary, ...prev].slice(0, 5));
    } catch (error) {
      console.error('Error:', error);
    }
    setIsProcessing(false);
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(summary);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleReset = () => {
    setIsProcessing(false);
    setSummary('');
    setText('');
    setUrl('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className={`min-h-screen ${darkMode ? 'dark bg-gray-800' : 'bg-gray-50'}`}>
    <header className={`${darkMode ? 'bg-gray-700' : 'bg-white'} shadow-sm`}>
      <div className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
        <div>
          <h1 className={`text-3xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Briefy</h1>
          <p className={`${darkMode ? 'text-gray-300' : 'text-gray-500'} mt-1`}>Get to the point, fast</p>
        </div>
        <button 
          className={`p-2 rounded-lg ${darkMode ? 'bg-gray-600 hover:bg-gray-500' : 'bg-gray-200 hover:bg-gray-300'}`}
          onClick={() => setDarkMode(!darkMode)}
        >
          {darkMode ? '☀️' : '🌙'}
        </button>
      </div>
    </header>

    <main className="max-w-7xl mx-auto px-4 py-8">
      <div className={`${darkMode ? 'bg-gray-700' : 'bg-white'} rounded-lg shadow p-6`}>
        <div className="space-y-4">
          <div className="flex gap-2">
            <input
              type="url"
              className={`flex-1 p-2 border rounded-lg ${
                darkMode 
                  ? 'bg-gray-600 text-white border-gray-600 placeholder-gray-400' 
                  : 'bg-white text-gray-700 border-gray-300'
              }`}
              placeholder="Enter URL to summarize..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <button
              className={`px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700`}
              onClick={() => setText('')}
            >
              <Link className="h-5 w-5" />
            </button>
          </div>

          <textarea
            className={`w-full h-48 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
              ${darkMode 
                ? 'bg-gray-600 text-white border-gray-600 placeholder-gray-400' 
                : 'bg-white text-gray-700 border-gray-300'
              }`}
            placeholder="Or paste your text here..."
            value={text}
            onChange={(e) => {
              setText(e.target.value);
              setUrl('');
            }}
          />
          
          <div
            className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer 
              ${darkMode ? 'border-gray-600' : 'border-gray-300'}`}
            onClick={() => fileInputRef.current?.click()}
          >
            <Upload className={`mx-auto h-12 w-12 ${darkMode ? 'text-gray-400' : 'text-gray-400'}`} />
            <p className={`mt-2 text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
              Or upload a file (PDF, DOCX)
            </p>
            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              accept=".pdf,.docx"
              onChange={handleFileUpload}
            />
          </div>

          <div className="flex items-center gap-6">
            <label className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>Summary Type:</label>
            <div className="flex gap-4">
              {[
                { id: 'brief', label: 'Brief Overview', value: 'brief' },
                { id: 'detailed', label: 'Detailed Analysis', value: 'detailed' }
              ].map((option) => (
                <div key={option.id} className="flex items-center">
                  <input
                    type="radio"
                    id={option.id}
                    name="summaryType"
                    value={option.value}
                    checked={summaryRatio === option.value}
                    onChange={(e) => setSummaryRatio(e.target.value)}
                    className="mr-2"
                  />
                  <label htmlFor={option.id} className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                    {option.label}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className="flex gap-2">
            <button
              className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
              onClick={handleSummarize}
              disabled={isProcessing || (!text && !url)}
            >
              {isProcessing ? 'Processing...' : 'Briefy it!'}
            </button>
            <button
              className={`px-4 py-2 rounded-lg ${
                darkMode 
                  ? 'bg-gray-600 text-gray-300 hover:bg-gray-500' 
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
              onClick={handleReset}
            >
              <RefreshCw className="h-5 w-5" />
            </button>
          </div>
        </div>

        {summary && (
          <div className="mt-8 space-y-4">
            <div className={`${darkMode ? 'bg-gray-600' : 'bg-gray-50'} p-4 rounded-lg`}>
              <div className="flex justify-between items-center mb-2">
                <h2 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Summary</h2>
                <div className="space-x-2">
                  <button
                    className={`p-2 ${darkMode ? 'text-gray-300 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}
                    onClick={handleCopy}
                    title={copySuccess ? 'Copied!' : 'Copy to clipboard'}
                  >
                    <Copy className="h-5 w-5" />
                  </button>
                  <button className={`p-2 ${darkMode ? 'text-gray-300 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}>
                    <Share2 className="h-5 w-5" />
                  </button>
                </div>
              </div>
              <p className={`${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>{summary}</p>
              {copySuccess && (
                <div className="text-sm text-green-600 mt-2">
                  Copied to clipboard!
                </div>
              )}
            </div>
          </div>
        )}

        {summaryHistory.length > 0 && (
          <div className="mt-8">
            <div className="flex justify-between items-center mb-4">
              <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Recent Summaries</h3>
              <button
                onClick={() => setSummaryHistory([])}
                className={`text-sm ${darkMode ? 'text-gray-400 hover:text-gray-300' : 'text-gray-500 hover:text-gray-700'}`}
              >
                Clear History
              </button>
            </div>
            <div className="space-y-4">
              {summaryHistory.map(item => (
                <div key={item.id} className={`${darkMode ? 'bg-gray-600' : 'bg-gray-50'} p-4 rounded-lg`}>
                  <div className="flex justify-between text-sm mb-2">
                    <span className={darkMode ? 'text-gray-300' : 'text-gray-500'}>{item.type} Summary</span>
                    <div className="flex items-center gap-2">
                      <span className={darkMode ? 'text-gray-300' : 'text-gray-500'}>{item.timestamp}</span>
                      <button
                        onClick={() => navigator.clipboard.writeText(item.content)}
                        className={`${darkMode ? 'text-gray-300 hover:text-white' : 'text-gray-600 hover:text-gray-900'}`}
                      >
                        <Copy className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                  <p className={darkMode ? 'text-gray-300' : 'text-gray-700'}>{item.content}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
    </div>
  );
};

export default App;