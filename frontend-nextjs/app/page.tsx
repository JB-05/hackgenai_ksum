'use client';

import React, { useState, useEffect } from 'react';
import { WorkflowSteps } from '@/components/WorkflowSteps';
import { Phase1PromptInput } from '@/components/Phase1PromptInput';
import { Phase2EnhancedStory } from '@/components/Phase2EnhancedStory';
import { Phase3Confirmation } from '@/components/Phase3Confirmation';
import { Phase4Generation } from '@/components/Phase4Generation';
import { Phase5Results } from '@/components/Phase5Results';
import { workflowAPI, EnhancedPromptResponse, FinalVideoResponse } from '@/lib/api';
import { checkBackendHealth } from '@/lib/health-check';
import toast from 'react-hot-toast';

type WorkflowPhase = 'prompt_input' | 'enhancement' | 'confirmation' | 'generation' | 'completed';

interface WorkflowData {
  workflowId: string;
  enhancedStory: EnhancedPromptResponse | null;
  finalResult: FinalVideoResponse | null;
  originalPrompt?: { userPrompt: string; title?: string; maxScenes: number };
}

export default function Home() {
  const [currentPhase, setCurrentPhase] = useState<WorkflowPhase>('prompt_input');
  const [workflowData, setWorkflowData] = useState<WorkflowData>({
    workflowId: '',
    enhancedStory: null,
    finalResult: null,
    originalPrompt: undefined,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [isRegenerating, setIsRegenerating] = useState(false);

  const workflowSteps = [
    {
      id: 'prompt_input',
      title: 'Prompt Input',
      description: 'Enter your story idea',
      status: currentPhase === 'prompt_input' ? 'active' : 
              currentPhase === 'enhancement' || currentPhase === 'confirmation' || currentPhase === 'generation' || currentPhase === 'completed' ? 'completed' : 'pending',
    },
    {
      id: 'enhancement',
      title: 'Enhancement',
      description: 'AI enhances your story',
      status: currentPhase === 'enhancement' ? 'active' : 
              currentPhase === 'confirmation' || currentPhase === 'generation' || currentPhase === 'completed' ? 'completed' : 'pending',
    },
    {
      id: 'confirmation',
      title: 'Confirmation',
      description: 'Review and confirm',
      status: currentPhase === 'confirmation' ? 'active' : 
              currentPhase === 'generation' || currentPhase === 'completed' ? 'completed' : 'pending',
    },
    {
      id: 'generation',
      title: 'Generation',
      description: 'Creating your video',
      status: currentPhase === 'generation' ? 'active' : 
              currentPhase === 'completed' ? 'completed' : 'pending',
    },
    {
      id: 'completed',
      title: 'Completed',
      description: 'Download your video',
      status: currentPhase === 'completed' ? 'completed' : 'pending',
    },
  ];

  // Check API health on mount
  useEffect(() => {
    const checkHealth = async () => {
      const healthStatus = await checkBackendHealth();
      if (!healthStatus.isHealthy) {
        toast.error(healthStatus.message);
      }
    };
    checkHealth();
  }, []);

  const handlePromptSubmit = async (data: { userPrompt: string; title?: string; maxScenes: number }) => {
    setIsLoading(true);
    try {
      // Create workflow
      const workflowResponse = await workflowAPI.createWorkflow();
      const workflowId = workflowResponse.workflow_id;

      // Enhance prompt
      const enhancedStory = await workflowAPI.enhancePrompt(workflowId, {
        user_prompt: data.userPrompt,
        title: data.title,
        max_scenes: data.maxScenes,
      });

      setWorkflowData({
        workflowId,
        enhancedStory,
        finalResult: null,
        originalPrompt: data,
      });

      setCurrentPhase('enhancement');
      toast.success('Story enhanced successfully!');
    } catch (error) {
      console.error('Error in prompt enhancement:', error);
      toast.error('Failed to enhance prompt. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleProceedToConfirmation = () => {
    setCurrentPhase('confirmation');
  };

  const handleBackToPrompt = () => {
    setCurrentPhase('prompt_input');
    setWorkflowData({
      workflowId: '',
      enhancedStory: null,
      finalResult: null,
      originalPrompt: undefined,
    });
  };

  const handleRegenerate = async () => {
    if (!workflowData.originalPrompt || !workflowData.workflowId) return;

    setIsRegenerating(true);
    try {
      // Re-enhance the same prompt
      const enhancedStory = await workflowAPI.enhancePrompt(workflowData.workflowId, {
        user_prompt: workflowData.originalPrompt.userPrompt,
        title: workflowData.originalPrompt.title,
        max_scenes: workflowData.originalPrompt.maxScenes,
      });

      setWorkflowData(prev => ({
        ...prev,
        enhancedStory,
      }));

      toast.success('Story regenerated successfully!');
    } catch (error) {
      console.error('Error regenerating story:', error);
      toast.error('Failed to regenerate story. Please try again.');
    } finally {
      setIsRegenerating(false);
    }
  };

  const handleConfirmGeneration = async () => {
    if (!workflowData.enhancedStory) return;

    setIsLoading(true);
    try {
      // Confirm generation
      await workflowAPI.confirmGeneration(workflowData.workflowId, {
        enhanced_story: workflowData.enhancedStory.enhanced_story,
        story_title: workflowData.enhancedStory.story_title,
        max_scenes: workflowData.enhancedStory.estimated_scenes,
        proceed: true,
      });

      setCurrentPhase('generation');
      toast.success('Generation started!');
    } catch (error) {
      console.error('Error confirming generation:', error);
      toast.error('Failed to start generation. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerationComplete = async () => {
    try {
      // Get final result
      const finalResult = await workflowAPI.getResult(workflowData.workflowId);
      
      setWorkflowData(prev => ({
        ...prev,
        finalResult,
      }));

      setCurrentPhase('completed');
      toast.success('Video generation completed!');
    } catch (error) {
      console.error('Error getting final result:', error);
      toast.error('Failed to get final result. Please try again.');
    }
  };

  const handleGenerationError = (error: string) => {
    toast.error(error);
    setCurrentPhase('confirmation');
  };

  const handleStartNew = () => {
    setCurrentPhase('prompt_input');
    setWorkflowData({
      workflowId: '',
      enhancedStory: null,
      finalResult: null,
      originalPrompt: undefined,
    });
  };

  const renderCurrentPhase = () => {
    switch (currentPhase) {
      case 'prompt_input':
        return (
          <Phase1PromptInput
            onNext={handlePromptSubmit}
            isLoading={isLoading}
          />
        );

      case 'enhancement':
        return workflowData.enhancedStory ? (
          <Phase2EnhancedStory
            enhancedStory={workflowData.enhancedStory}
            onProceed={handleProceedToConfirmation}
            onBack={handleBackToPrompt}
            onRegenerate={handleRegenerate}
            isRegenerating={isRegenerating}
          />
        ) : null;

      case 'confirmation':
        return workflowData.enhancedStory ? (
          <Phase3Confirmation
            enhancedStory={workflowData.enhancedStory}
            onConfirm={handleConfirmGeneration}
            onBack={() => setCurrentPhase('enhancement')}
          />
        ) : null;

      case 'generation':
        return (
          <Phase4Generation
            workflowId={workflowData.workflowId}
            onComplete={handleGenerationComplete}
            onError={handleGenerationError}
          />
        );

      case 'completed':
        return workflowData.finalResult ? (
          <Phase5Results
            result={workflowData.finalResult}
            onStartNew={handleStartNew}
          />
        ) : null;

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">🎬</span>
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Story-to-Video Generator
                </h1>
                <p className="text-sm text-gray-600">AI-powered video creation</p>
              </div>
            </div>
            <div className="text-sm text-gray-500">
              Phase {workflowSteps.findIndex(step => step.id === currentPhase) + 1} of 5
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Workflow Steps */}
        <div className="mb-8">
          <WorkflowSteps
            steps={workflowSteps}
            currentStep={currentPhase}
          />
        </div>

        {/* Phase Content */}
        <div className="min-h-[600px]">
          {renderCurrentPhase()}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white/80 backdrop-blur-sm border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-600">
            <p>Transform your story ideas into professional videos with AI</p>
            <p className="mt-1">Powered by OpenAI, ElevenLabs, and Suno.ai</p>
          </div>
        </div>
      </footer>
    </div>
  );
} 