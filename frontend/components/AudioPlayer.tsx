'use client';

import { useState, useRef } from 'react';

interface AudioPlayerProps {
    song: any;
}

export default function AudioPlayer({ song }: AudioPlayerProps) {
    const [isPlaying, setIsPlaying] = useState(false);
    const audioRef = useRef<HTMLAudioElement>(null);

    const togglePlay = () => {
        if (audioRef.current) {
            if (isPlaying) {
                audioRef.current.pause();
            } else {
                audioRef.current.play();
            }
            setIsPlaying(!isPlaying);
        }
    };

    const downloadSong = () => {
        if (song.result_url) {
            const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
            window.open(`${API_URL}${song.result_url}`, '_blank');
        }
    };

    return (
        <div className="space-y-6">
            {/* Song Info */}
            <div className="bg-white/5 rounded-lg p-4">
                <h3 className="text-xl font-bold text-white mb-2">
                    {song.lyrics?.title || 'Untitled'}
                </h3>
                <p className="text-gray-400 text-sm">
                    BPM: {song.lyrics?.bpm_suggestion || 'N/A'}
                </p>
            </div>

            {/* Audio Player */}
            <div className="bg-white/5 rounded-lg p-6 space-y-4">
                <audio
                    ref={audioRef}
                    src={`${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}${song.result_url}`}
                    onEnded={() => setIsPlaying(false)}
                />

                <button
                    onClick={togglePlay}
                    className="w-full py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all flex items-center justify-center gap-2"
                >
                    {isPlaying ? (
                        <>
                            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M5 4h3v12H5V4zm7 0h3v12h-3V4z" />
                            </svg>
                            Pause
                        </>
                    ) : (
                        <>
                            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
                            </svg>
                            Play
                        </>
                    )}
                </button>

                <button
                    onClick={downloadSong}
                    className="w-full py-3 bg-white/10 text-white font-medium rounded-lg hover:bg-white/20 transition-all flex items-center justify-center gap-2"
                >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    Download
                </button>
            </div>

            {/* Lyrics Display */}
            {song.lyrics?.lyrics && (
                <div className="bg-white/5 rounded-lg p-6 max-h-96 overflow-y-auto">
                    <h4 className="text-lg font-bold text-white mb-4">Lyrics</h4>
                    <div className="space-y-4">
                        {song.lyrics.lyrics.map((section: any, index: number) => (
                            <div key={index} className="space-y-1">
                                <p className="text-purple-400 font-semibold text-sm">
                                    [{section.section}]
                                </p>
                                <p className="text-gray-300 whitespace-pre-wrap">
                                    {section.text}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
