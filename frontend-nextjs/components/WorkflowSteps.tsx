import React from 'react';
import { Check, Circle, Clock } from 'lucide-react';
import { cn } from '@/lib/utils';

interface WorkflowStep {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'active' | 'completed' | 'error';
}

interface WorkflowStepsProps {
  steps: WorkflowStep[];
  currentStep: string;
}

export function WorkflowSteps({ steps, currentStep }: WorkflowStepsProps) {
  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="flex items-center justify-between">
        {steps.map((step, index) => {
          const isActive = step.id === currentStep;
          const isCompleted = step.status === 'completed';
          const isPending = step.status === 'pending';
          const isError = step.status === 'error';

          return (
            <React.Fragment key={step.id}>
              <div className="flex flex-col items-center">
                <div
                  className={cn(
                    'w-12 h-12 rounded-full flex items-center justify-center border-2 transition-all duration-300',
                    {
                      'bg-primary border-primary text-white': isActive,
                      'bg-green-500 border-green-500 text-white': isCompleted,
                      'bg-gray-200 border-gray-300 text-gray-500': isPending,
                      'bg-red-500 border-red-500 text-white': isError,
                    }
                  )}
                >
                  {isCompleted ? (
                    <Check className="w-6 h-6" />
                  ) : isError ? (
                    <Circle className="w-6 h-6" />
                  ) : isActive ? (
                    <Clock className="w-6 h-6 animate-pulse" />
                  ) : (
                    <span className="text-sm font-medium">{index + 1}</span>
                  )}
                </div>
                <div className="mt-2 text-center max-w-24">
                  <p
                    className={cn('text-sm font-medium', {
                      'text-primary': isActive,
                      'text-green-600': isCompleted,
                      'text-gray-500': isPending,
                      'text-red-600': isError,
                    })}
                  >
                    {step.title}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">{step.description}</p>
                </div>
              </div>
              {index < steps.length - 1 && (
                <div
                  className={cn(
                    'flex-1 h-0.5 transition-all duration-300',
                    {
                      'bg-primary': isCompleted,
                      'bg-gray-300': !isCompleted,
                    }
                  )}
                />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
} 