{{- define "nt114-fl.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "nt114-fl.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s" (include "nt114-fl.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{- define "nt114-fl.labels" -}}
app.kubernetes.io/name: {{ include "nt114-fl.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: Helm
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" }}
{{- end -}}

{{- define "nt114-fl.appImage" -}}
{{- $repo := .Values.image.repository | default "" -}}
{{- if or (eq $repo "") (contains "YOUR_ACR_NAME" $repo) (hasPrefix "/" $repo) -}}
{{- fail "image.repository is invalid. Set it via --set-string image.repository=<acr-login-server>/project-nt114 or update values-aks.yaml." -}}
{{- end -}}
{{- printf "%s:%s" $repo .Values.image.tag -}}
{{- end -}}