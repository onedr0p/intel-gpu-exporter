# intel-gpu-exporter

Get metrics from Intel GPUs

## Deployment

Runs on port 8080, does stuff, is hyperglued using python and intel_gpu_top

### Docker Compose

```yaml
version: "3.8"

services:
  intel-gpu-exporter:
    image: ghcr.io/onedr0p/intel-gpu-exporter:rolling
    container_name: intel-gpu-exporter
    restart: unless-stopped
    privileged: true
    pid: host
    ports:
      - 8080:8080
    volumes:
      - /dev/dri/:/dev/dri/
```

## Metrics

```bash
# HELP igpu_engines_blitter_0_busy Blitter 0 busy utilisation %
# TYPE igpu_engines_blitter_0_busy gauge
igpu_engines_blitter_0_busy 0.0
# HELP igpu_engines_blitter_0_sema Blitter 0 sema utilisation %
# TYPE igpu_engines_blitter_0_sema gauge
igpu_engines_blitter_0_sema 0.0
# HELP igpu_engines_blitter_0_wait Blitter 0 wait utilisation %
# TYPE igpu_engines_blitter_0_wait gauge
igpu_engines_blitter_0_wait 0.0
# HELP igpu_engines_render_3d_0_busy Render 3D 0 busy utilisation %
# TYPE igpu_engines_render_3d_0_busy gauge
igpu_engines_render_3d_0_busy 0.0
# HELP igpu_engines_render_3d_0_sema Render 3D 0 sema utilisation %
# TYPE igpu_engines_render_3d_0_sema gauge
igpu_engines_render_3d_0_sema 0.0
# HELP igpu_engines_render_3d_0_wait Render 3D 0 wait utilisation %
# TYPE igpu_engines_render_3d_0_wait gauge
igpu_engines_render_3d_0_wait 0.0
# HELP igpu_engines_video_0_busy Video 0 busy utilisation %
# TYPE igpu_engines_video_0_busy gauge
igpu_engines_video_0_busy 0.0
# HELP igpu_engines_video_0_sema Video 0 sema utilisation %
# TYPE igpu_engines_video_0_sema gauge
igpu_engines_video_0_sema 0.0
# HELP igpu_engines_video_0_wait Video 0 wait utilisation %
# TYPE igpu_engines_video_0_wait gauge
igpu_engines_video_0_wait 0.0
# HELP igpu_engines_video_enhance_0_busy Video Enhance 0 busy utilisation %
# TYPE igpu_engines_video_enhance_0_busy gauge
igpu_engines_video_enhance_0_busy 0.0
# HELP igpu_engines_video_enhance_0_sema Video Enhance 0 sema utilisation %
# TYPE igpu_engines_video_enhance_0_sema gauge
igpu_engines_video_enhance_0_sema 0.0
# HELP igpu_engines_video_enhance_0_wait Video Enhance 0 wait utilisation %
# TYPE igpu_engines_video_enhance_0_wait gauge
igpu_engines_video_enhance_0_wait 0.0
# HELP igpu_frequency_actual Frequency actual MHz
# TYPE igpu_frequency_actual gauge
igpu_frequency_actual 0.0
# HELP igpu_frequency_requested Frequency requested MHz
# TYPE igpu_frequency_requested gauge
igpu_frequency_requested 0.0
# HELP igpu_imc_bandwidth_reads IMC reads MiB/s
# TYPE igpu_imc_bandwidth_reads gauge
igpu_imc_bandwidth_reads 733.353818
# HELP igpu_imc_bandwidth_writes IMC writes MiB/s
# TYPE igpu_imc_bandwidth_writes gauge
igpu_imc_bandwidth_writes 166.044782
# HELP igpu_interrupts Interrupts/s
# TYPE igpu_interrupts gauge
igpu_interrupts 0.0
# HELP igpu_period Period ms
# TYPE igpu_period gauge
igpu_period 5000.241296
# HELP igpu_power_gpu GPU power W
# TYPE igpu_power_gpu gauge
igpu_power_gpu 0.0
# HELP igpu_power_package Package power W
# TYPE igpu_power_package gauge
igpu_power_package 5.480595
# HELP igpu_rc6 RC6 %
# TYPE igpu_rc6 gauge
igpu_rc6 99.999993
```
