'use client';

import { useState } from 'react';

interface SongGeneratorProps {
    onSongGenerated: (song: any) => void;
}

export default function SongGenerator({ onSongGenerated }: SongGeneratorProps) {
    const [topic, setTopic] = useState('');
    const [mood, setMood] = useState('hype');
    const [bpm, setBpm] = useState(140);
    const [energy, setEnergy] = useState('high');
    const [isGenerating, setIsGenerating] = useState(false);
    const [progress, setProgress] = useState(0);
    const [error, setError] = useState('');

    const handleGenerate = async () => {
        if (!topic.trim()) {
            setError('Please enter a song topic');
            return;
        }

        setIsGenerating(true);
        setProgress(0);
        setError('');

        try {
            // Call backend API
            const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
            const response = await fetch(`${API_URL}/api/v1/songs/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    topic,
                    mood,
                    bpm: parseInt(bpm.toString()),
                    energy,
                }),
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Failed to fetch ${API_URL}/api/v1/songs/generate: ${response.status} ${response.statusText} - ${errorText}`);
            }

            const { job_id } = await response.json();

            // Poll for status
            const pollInterval = setInterval(async () => {
                const statusResponse = await fetch(
                    `${API_URL}/api/v1/songs/${job_id}/status`
                );
                const status = await statusResponse.json();

                setProgress(status.progress || 0);

                if (status.status === 'completed') {
                    clearInterval(pollInterval);
                    setIsGenerating(false);
                    onSongGenerated(status);
                } else if (status.status === 'failed') {
                    clearInterval(pollInterval);
                    setIsGenerating(false);
                    setError('Song generation failed. Please try again.');
                }
            }, 2000);
        } catch (err: any) {
            setIsGenerating(false);
            setError(err.message || 'An error occurred');
        }
    };

    return (
        <div className="space-y-6">
            {/* Topic Input */}
            <div>
                <label className="block text-white text-sm font-medium mb-2">
                    Song Topic
                </label>
                <input
                    type="text"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    placeholder="e.g., Coding late at night"
                    className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    disabled={isGenerating}
                />
            </div>

            {/* Mood Select */}
            <div>
                <label className="block text-white text-sm font-medium mb-2">
                    Mood
                </label>
                <select
                    value={mood}
                    onChange={(e) => setMood(e.target.value)}
                    className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                    disabled={isGenerating}
                >
                    <option value="hype">Hype</option>
                    <option value="chill">Chill</option>
                    <option value="sad">Sad</option>
                    <option value="aggressive">Aggressive</option>
                    <option value="romantic">Romantic</option>
                </select>
            </div>

            {/* BPM Slider */}
            <div>
                <label className="block text-white text-sm font-medium mb-2">
                    BPM: {bpm}
                </label>
                <input
                    type="range"
                    min="60"
                    max="180"
                    value={bpm}
                    onChange={(e) => setBpm(parseInt(e.target.value))}
                    className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer accent-purple-500"
                    disabled={isGenerating}
                />
            </div>

            {/* Energy Select */}
            <div>
                <label className="block text-white text-sm font-medium mb-2">
                    Energy Level
                </label>
                <div className="grid grid-cols-3 gap-2">
                    {['low', 'medium', 'high'].map((level) => (
                        <button
                            key={level}
                            onClick={() => setEnergy(level)}
                            className={`py-2 px-4 rounded-lg font-medium transition-all ${energy === level
                                ? 'bg-purple-500 text-white'
                                : 'bg-white/5 text-gray-300 hover:bg-white/10'
                                }`}
                            disabled={isGenerating}
                        >
                            {level.charAt(0).toUpperCase() + level.slice(1)}
                        </button>
                    ))}
                </div>
            </div>

            {/* Generate Button */}
            <button
                onClick={handleGenerate}
                disabled={isGenerating}
                className="w-full py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {isGenerating ? 'Generating...' : 'Generate Song'}
            </button>

            {/* Progress Bar */}
            {isGenerating && (
                <div className="space-y-2">
                    <div className="w-full bg-white/10 rounded-full h-2">
                        <div
                            className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${progress}%` }}
                        />
                    </div>
                    <p className="text-center text-gray-300 text-sm">{progress}%</p>
                </div>
            )}

            {/* Error Message */}
            {error && (
                <div className="p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200">
                    {error}
                </div>
            )}
        </div>
    );
}
