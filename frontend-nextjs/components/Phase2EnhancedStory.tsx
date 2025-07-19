'use client';

import React from 'react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Check, ArrowLeft, BookOpen, Clock, Sparkles, RefreshCw } from 'lucide-react';
import { motion } from 'framer-motion';
import { EnhancedPromptResponse } from '@/lib/api';

interface Phase2EnhancedStoryProps {
  enhancedStory: EnhancedPromptResponse;
  onProceed: () => void;
  onBack: () => void;
  onRegenerate: () => void;
  isRegenerating?: boolean;
}

export function Phase2EnhancedStory({ enhancedStory, onProceed, onBack, onRegenerate, isRegenerating = false }: Phase2EnhancedStoryProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-6xl mx-auto space-y-6"
    >
      {/* Header */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-blue-600 rounded-full flex items-center justify-center">
              <Check className="w-8 h-8 text-white" />
            </div>
          </div>
          <CardTitle className="text-3xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
            Your Enhanced Story
          </CardTitle>
          <CardDescription className="text-lg text-gray-600">
            We've transformed your prompt into a complete narrative. Review it below and decide whether to proceed with video generation.
          </CardDescription>
        </CardHeader>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Original Prompt */}
        <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-lg">
              <BookOpen className="w-5 h-5 text-blue-600" />
              <span>Original Prompt</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="bg-gray-50 rounded-lg p-4 text-sm text-gray-700">
              "{enhancedStory.original_prompt}"
            </div>
          </CardContent>
        </Card>

        {/* Enhanced Story */}
        <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-xl">
              <Sparkles className="w-5 h-5 text-purple-600" />
              <span>{enhancedStory.story_title}</span>
            </CardTitle>
            <CardDescription className="flex items-center space-x-2 text-sm">
              <Clock className="w-4 h-4" />
              <span>Enhanced in {enhancedStory.processing_time.toFixed(2)}s</span>
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="prose prose-sm max-w-none">
              <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-6 border border-purple-200">
                <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                  {enhancedStory.enhanced_story}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Enhancement Details */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-lg">Enhancement Details</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                <span className="text-sm font-medium text-blue-800">Estimated Scenes</span>
                <span className="text-lg font-bold text-blue-600">{enhancedStory.estimated_scenes}</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <span className="text-sm font-medium text-green-800">Processing Time</span>
                <span className="text-lg font-bold text-green-600">{enhancedStory.processing_time.toFixed(2)}s</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                <span className="text-sm font-medium text-purple-800">Story Length</span>
                <span className="text-lg font-bold text-purple-600">{enhancedStory.enhanced_story.length} chars</span>
              </div>
            </div>
            <div className="space-y-3">
              <h4 className="font-medium text-gray-900">What We Enhanced:</h4>
              <ul className="space-y-2">
                {enhancedStory.enhancement_notes.map((note, index) => (
                  <li key={index} className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0" />
                    <span className="text-sm text-gray-700">{note}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardContent className="pt-6">
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              onClick={onBack}
              variant="outline"
              className="px-8 py-3 text-lg font-medium"
              disabled={isRegenerating}
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Start Over
            </Button>
            <Button
              onClick={onRegenerate}
              variant="outline"
              className="px-8 py-3 text-lg font-medium border-orange-500 text-orange-600 hover:bg-orange-50"
              disabled={isRegenerating}
            >
              <RefreshCw className={`w-5 h-5 mr-2 ${isRegenerating ? 'animate-spin' : ''}`} />
              {isRegenerating ? 'Regenerating...' : 'Regenerate'}
            </Button>
            <Button
              onClick={onProceed}
              className="px-8 py-3 text-lg font-medium bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-200"
              disabled={isRegenerating}
            >
              <Check className="w-5 h-5 mr-2" />
              Proceed with Generation
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
} 