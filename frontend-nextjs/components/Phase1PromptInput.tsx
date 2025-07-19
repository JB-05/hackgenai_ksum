'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Sparkles, Wand2, BookOpen, Video } from 'lucide-react';
import { motion } from 'framer-motion';

interface Phase1PromptInputProps {
  onNext: (data: { userPrompt: string; title?: string; maxScenes: number }) => void;
  isLoading?: boolean;
}

export function Phase1PromptInput({ onNext, isLoading }: Phase1PromptInputProps) {
  const [userPrompt, setUserPrompt] = useState('');
  const [title, setTitle] = useState('');
  const [maxScenes, setMaxScenes] = useState(4);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (userPrompt.trim().length < 10) return;
    
    onNext({
      userPrompt: userPrompt.trim(),
      title: title.trim() || undefined,
      maxScenes,
    });
  };

  const examplePrompts = [
    "A young wizard discovers a magical library hidden in the clouds",
    "A robot learns to paint and creates the most beautiful artwork",
    "A time traveler visits ancient Egypt and helps build the pyramids",
    "A talking cat leads children on an adventure through a secret garden",
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-4xl mx-auto"
    >
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
              <Sparkles className="w-8 h-8 text-white" />
            </div>
          </div>
          <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Tell Us Your Story
          </CardTitle>
          <CardDescription className="text-lg text-gray-600 max-w-2xl mx-auto">
            Share your story idea and our AI will transform it into a complete narrative, 
            then create a professional video with images, voice, and music.
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="prompt" className="text-sm font-medium text-gray-700">
                Your Story Prompt *
              </label>
              <textarea
                id="prompt"
                value={userPrompt}
                onChange={(e) => setUserPrompt(e.target.value)}
                placeholder="Describe your story idea here... For example: 'A young explorer discovers a hidden cave with ancient magical artifacts'"
                className="textarea min-h-[120px] resize-none"
                required
                minLength={10}
              />
              <p className="text-xs text-gray-500">
                {userPrompt.length}/500 characters (minimum 10 required)
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label htmlFor="title" className="text-sm font-medium text-gray-700">
                  Story Title (Optional)
                </label>
                <input
                  id="title"
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Leave empty for auto-generation"
                  className="input"
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="scenes" className="text-sm font-medium text-gray-700">
                  Number of Scenes
                </label>
                <select
                  id="scenes"
                  value={maxScenes}
                  onChange={(e) => setMaxScenes(Number(e.target.value))}
                  className="input"
                >
                  <option value={3}>3 scenes</option>
                  <option value={4}>4 scenes</option>
                  <option value={5}>5 scenes</option>
                  <option value={6}>6 scenes</option>
                </select>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">
                Example Prompts
              </label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {examplePrompts.map((prompt, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => setUserPrompt(prompt)}
                    className="text-left p-3 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md border border-gray-200 hover:border-gray-300 transition-colors"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <Wand2 className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                <div className="text-sm text-blue-800">
                  <p className="font-medium mb-1">How it works:</p>
                  <ol className="list-decimal list-inside space-y-1 text-blue-700">
                    <li>We'll enhance your prompt into a complete story</li>
                    <li>You'll review the enhanced version</li>
                    <li>If you approve, we'll generate a professional video</li>
                    <li>Download your video with images, voice, and music</li>
                  </ol>
                </div>
              </div>
            </div>

            <div className="flex justify-center">
              <Button
                type="submit"
                disabled={userPrompt.trim().length < 10 || isLoading}
                className="px-8 py-3 text-lg font-medium bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-200"
              >
                {isLoading ? (
                  <div className="flex items-center space-x-2">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>Enhancing Prompt...</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-2">
                    <Sparkles className="w-5 h-5" />
                    <span>Enhance My Story</span>
                  </div>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </motion.div>
  );
} 