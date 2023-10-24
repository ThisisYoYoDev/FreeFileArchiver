<template>
  <div class="home">
    <div class="title">
      <h1>File Uploader</h1>
      <div class="line"></div>
    </div>


    <div class="container">
      <div class="upload">
        <input type="file" @change="handleFileUpload" />
        <button @click="uploadFile">Upload</button>
      </div>
    </div>

    <div>
      <label for="progress-bar">0%</label>
      <progress id="progress-bar" value="0" max="100"></progress>
    </div>

    <div v-if="uploadedFile">
      <h2>Uploaded File:</h2>
      <p>Name: {{ uploadedFile.name }}</p>
      <p>Size: {{ humanFileSize(uploadedFile.size) }}</p>
    </div>

    <div v-if="downloadLink">
      <h2>The download url has been copied to your clipboard</h2>
      <p>{{ downloadLink }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      uploadedFile: null,
      downloadLink: null,
    };
  },
  methods: {
    handleFileUpload(event) {
      this.uploadedFile = event.target.files[0];
    },
    async uploadFile() {
      const url = 'http://127.0.0.1:8000/upload';

      const headers = {
        'Content-Disposition': `attachment; filename="${this.uploadedFile.name}"`,
      };

      const formData = new FormData();
      formData.append('file', this.uploadedFile);

      const config = {
        onUploadProgress: function(progressEvent) {
          const percentCompleted = Math.round((progressEvent.loaded / progressEvent.total)*100);

          const progressBar = document.getElementById("progress-bar");
          progressBar.value = percentCompleted;

          const label = document.querySelector("label[for=progress-bar]");
          label.textContent = percentCompleted + "%";
        },
        headers,
      }

      const response = await axios.post(url, formData, config)

      this.downloadLink = `http://127.0.0.1:8000/download/${response.data.id}`;
      await navigator.clipboard.writeText(this.downloadLink);
    },

    humanFileSize(bytes, si=true, dp=1) {
      const thresh = si ? 1000 : 1024;

      if (Math.abs(bytes) < thresh) {
        return bytes + ' B';
      }

      const units = si
        ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
      let u = -1;
      const r = 10**dp;

      do {
        bytes /= thresh;
        ++u;
      } while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1);


      return bytes.toFixed(dp) + ' ' + units[u];
    },
  },
};
</script>

<!-- <style>
.home {
  overflow: hidden;
}
.home .title {
  position: absolute;
  top: 20px;
  left: 20px;
}

.home .line {
  width: 100%;
  height: 2px;
  background-color: #444;
  margin-top: 6px;
}

.home .container {
  position: absolute;
  width: 700px;
  height: 400px;
  border-radius: 30px;
  border: 2px solid #fff;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.home .container .upload {
  width: 400px;
  height: 300px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 5%;
  border: 2px dotted #fff;
}



</style> -->
