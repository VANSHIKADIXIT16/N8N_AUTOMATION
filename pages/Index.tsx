import { useEffect, useState } from "react";

export default function Index() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-100 to-slate-200">
      <div className="text-center">
        <h1 className="text-2xl font-semibold text-slate-800 flex items-center justify-center gap-3">
          WorkflowAI - Home
        </h1>
        <p className="mt-4 text-slate-600 max-w-md">
          Welcome to WorkflowAI! Use the login or signup to get started.
        </p>
      </div>
    </div>
  );
}
