import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../lib/api/client";
import { Assessment, AssessmentResultResponse, MetadataForm } from "../lib/types";

interface UploadUrlResponse {
  upload_url: string;
  file_key: string;
  assessment_id: string;
}

export function useSubmitAssessment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ file, metadata }: { file: File; metadata: MetadataForm }) => {
      // 1. Get pre-signed upload URL from backend
      const ext = file.name.split(".").pop() || "csv";
      const { upload_url, file_key, assessment_id } = await api.post<UploadUrlResponse>(
        "/api/v1/assess/upload-url",
        {
          filename: file.name,
          file_format: ext,
        }
      );

      // 2. Upload file directly to S3 via pre-signed PUT
      const uploadResponse = await fetch(upload_url, {
        method: "PUT",
        headers: {
          "Content-Type": file.type || "application/octet-stream",
        },
        body: file,
      });

      if (!uploadResponse.ok) {
        throw new Error("Failed to upload dataset file to object storage.");
      }

      // 3. Submit assessment request to backend
      const submissionResponse = await api.post<{ assessment_id: string; status: string }>(
        "/api/v1/assess",
        {
          file_key,
          metadata,
        }
      );

      return {
        assessment_id,
        status: submissionResponse.status,
      };
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["assessments"] });
    },
  });
}

export function useAssessments(skip = 0, limit = 10) {
  return useQuery<Assessment[]>({
    queryKey: ["assessments", skip, limit],
    queryFn: () => api.get<Assessment[]>(`/api/v1/assess/?skip=${skip}&limit=${limit}`),
  });
}

export function useAssessmentStatus(assessmentId: string) {
  return useQuery<Assessment | AssessmentResultResponse>({
    queryKey: ["assessment", assessmentId],
    queryFn: () => api.get<Assessment | AssessmentResultResponse>(`/api/v1/assess/${assessmentId}`),
    refetchInterval: (query) => {
      const data = query.state.data;
      if (data && "status" in data && (data.status === "queued" || data.status === "processing")) {
        return 3000; // Poll every 3 seconds while processing
      }
      return false; // Stop polling on complete/failed
    },
  });
}
