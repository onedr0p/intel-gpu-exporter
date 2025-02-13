from prometheus_client import start_http_server, Gauge
import os
import subprocess
import json
import logging

gpu_period = Gauge("gpu_period", "Period ms")

gpu_frequency_actual = Gauge("gpu_frequency_actual", "Frequency actual MHz")
gpu_frequency_requested = Gauge("gpu_frequency_requested", "Frequency requested MHz")

gpu_interrupts = Gauge("gpu_interrupts", "Interrupts/s")

gpu_rc6 = Gauge("gpu_rc6", "RC6 %")

gpu_imc_bandwidth_reads = Gauge("gpu_imc_bandwidth_reads", "IMC reads MiB/s")
gpu_imc_bandwidth_writes = Gauge("gpu_imc_bandwidth_writes", "IMC writes MiB/s")

gpu_engines_render_3d_busy = Gauge("gpu_engines_render_3d_busy", "Render 3D 0 busy utilisation %")
gpu_engines_render_3d_sema = Gauge("gpu_engines_render_3d_sema", "Render 3D 0 sema utilisation %")
gpu_engines_render_3d_wait = Gauge("gpu_engines_render_3d_wait", "Render 3D 0 wait utilisation %")

gpu_engines_blitter_busy = Gauge("gpu_engines_blitter_busy", "Blitter 0 busy utilisation %")
gpu_engines_blitter_sema = Gauge("gpu_engines_blitter_sema", "Blitter 0 sema utilisation %")
gpu_engines_blitter_wait = Gauge("gpu_engines_blitter_wait", "Blitter 0 wait utilisation %")

gpu_engines_video_enhance_busy = Gauge("gpu_engines_video_enhance_busy", "Video Enhance 0 busy utilisation %")
gpu_engines_video_enhance_sema = Gauge("gpu_engines_video_enhance_sema", "Video Enhance 0 sema utilisation %")
gpu_engines_video_enhance_wait = Gauge("gpu_engines_video_enhance_wait", "Video Enhance 0 wait utilisation %")

gpu_engines_video_busy = Gauge("gpu_engines_video_busy", "Video 0 busy utilisation %")
gpu_engines_video_sema = Gauge("gpu_engines_video_sema", "Video 0 sema utilisation %")
gpu_engines_video_wait = Gauge("gpu_engines_video_wait", "Video 0 wait utilisation %")

gpu_engines_compute_busy = Gauge("gpu_engines_compute_busy", "Compute busy utilisation %")
gpu_engines_compute_sema = Gauge("gpu_engines_compute_sema", "Compute sema utilisation %")
gpu_engines_compute_wait = Gauge("gpu_engines_compute_wait", "Compute wait utilisation %")

gpu_power_gpu = Gauge("gpu_power_gpu", "GPU power W")
gpu_power_package = Gauge("gpu_power_package", "Package power W")

def update(data):
    def get_engine(name):
        engines = data.get("engines", {})
        return engines.get(name, engines.get(name + "/0", {}))

    period_data = data.get("period", {})
    gpu_period.set(period_data.get("duration", 0))

    freq = data.get("frequency", {})
    gpu_frequency_actual.set(freq.get("actual", 0))
    gpu_frequency_requested.set(freq.get("requested", 0))

    interrupts = data.get("interrupts", {})
    gpu_interrupts.set(interrupts.get("count", 0))

    rc6 = data.get("rc6", {})
    gpu_rc6.set(rc6.get("value", 0))

    imc = data.get("imc-bandwidth", {})
    gpu_imc_bandwidth_reads.set(imc.get("reads", 0))
    gpu_imc_bandwidth_writes.set(imc.get("writes", 0))

    render3d = get_engine("Render/3D")
    gpu_engines_render_3d_busy.set(render3d.get("busy", 0.0))
    gpu_engines_render_3d_sema.set(render3d.get("sema", 0.0))
    gpu_engines_render_3d_wait.set(render3d.get("wait", 0.0))

    blitter = get_engine("Blitter")
    gpu_engines_blitter_busy.set(blitter.get("busy", 0.0))
    gpu_engines_blitter_sema.set(blitter.get("sema", 0.0))
    gpu_engines_blitter_wait.set(blitter.get("wait", 0.0))

    video = get_engine("Video")
    gpu_engines_video_busy.set(video.get("busy", 0.0))
    gpu_engines_video_sema.set(video.get("sema", 0.0))
    gpu_engines_video_wait.set(video.get("wait", 0.0))

    video_enhance = get_engine("VideoEnhance")
    gpu_engines_video_enhance_busy.set(video_enhance.get("busy", 0.0))
    gpu_engines_video_enhance_sema.set(video_enhance.get("sema", 0.0))
    gpu_engines_video_enhance_wait.set(video_enhance.get("wait", 0.0))

    compute = get_engine("Compute")
    gpu_engines_compute_busy.set(compute.get("busy", 0.0))
    gpu_engines_compute_sema.set(compute.get("sema", 0.0))
    gpu_engines_compute_wait.set(compute.get("wait", 0.0))

    gpu_power_gpu.set(data.get("power", {}).get("GPU", 0))
    gpu_power_package.set(data.get("power", {}).get("Package", 0))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s") 
    
    start_http_server(8080)
    
    period = int(os.getenv("REFRESH_PERIOD_MS", 10000))
    cmd = f"intel_gpu_top -J -s {period}"
    
    process = subprocess.Popen(
        cmd.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    logging.info(f"Started: {cmd}")

    buffer = ""
    decoder = json.JSONDecoder()

    while process.poll() is None:
        line = process.stdout.readline()
        if not line:
            continue
        buffer += line
        
        if buffer.startswith("["):
            buffer = buffer[1:]
        
        buffer = buffer.lstrip()
        
        while buffer:
            try:
                obj, idx = decoder.raw_decode(buffer)
                update(obj)
                buffer = buffer[idx:].lstrip(",")
            except json.JSONDecodeError:
                break

    process.kill()
    if process.returncode != 0:
        error = process.stderr.read()
        logging.error(f"Error: {error}")