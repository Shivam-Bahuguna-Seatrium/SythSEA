export const routes = {
  intake: "/datasets/intakes",
  jobs: "/training/jobs",
  generationRuns: "/generation/runs",
  models: "/chat/models",
  conversations: "/chat/conversations",
  readiness: "/readiness",
  lineage: (artifactId: string) => `/artifacts/${artifactId}/lineage`,
};