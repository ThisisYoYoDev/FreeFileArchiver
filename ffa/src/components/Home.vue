<template>
  <div class="home">
    <h1>File Uploader</h1>
    <input type="file" @change="handleFileUpload" />
    <button @click="uploadFile">Upload</button>

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

      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        headers,
      });

      this.downloadLink = `http://127.0.0.1:8000/download/${(await response.json()).id}`;
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
