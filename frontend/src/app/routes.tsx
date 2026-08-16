import { Route, Routes } from "react-router-dom";

import { ChatPage } from "../features/chat/ChatPage";
import { EvidencePage } from "../features/evidence/EvidencePage";
import { GenerationPage } from "../features/generation/GenerationPage";
import { DatasetIntakePage } from "../features/intake/DatasetIntakePage";
import { OverviewPage } from "../features/overview/OverviewPage";
import { TrainingPage } from "../features/training/TrainingPage";

export function WorkbenchRoutes() {
  return (
    <Routes>
      <Route path="/" element={<OverviewPage />} />
      <Route path="/intake" element={<DatasetIntakePage />} />
      <Route path="/generation" element={<GenerationPage />} />
      <Route path="/training" element={<TrainingPage />} />
      <Route path="/chat" element={<ChatPage />} />
      <Route path="/evidence" element={<EvidencePage />} />
    </Routes>
  );
}