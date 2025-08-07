import { Loader2 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
  text?: string;
}

export default function LoadingSpinner({ size = "md", text = "Ładowanie..." }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: "w-4 h-4",
    md: "w-8 h-8", 
    lg: "w-12 h-12"
  };

  return (
    <Card className="bg-white/70 backdrop-blur-sm border-white/20">
      <CardContent className="p-12 text-center">
        <Loader2 className={`${sizeClasses[size]} mx-auto text-blue-600 animate-spin mb-4`} />
        <p className="text-gray-600 font-medium">{text}</p>
      </CardContent>
    </Card>
  );
}
