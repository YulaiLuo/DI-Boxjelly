const downloadFileUtil = {
  getBlob(url) {
    return new Promise((resolve) => {
      const xhr = new XMLHttpRequest();

      xhr.open('GET', url, true);
      xhr.responseType = 'blob';
      xhr.onload = () => {
        if (xhr.status === 200) {
          resolve(xhr.response);
        }
      };

      xhr.send();
    });
  },

  saveAs(blob, filename) {
    let link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = filename;
    link.click();

    window.URL.revokeObjectURL(link.href);
    link = null;
  },

  load(file) {
    this.getBlob(file.url).then((blob) => {
      this.saveAs(blob, file.name);
    });
  },
};

export default downloadFileUtil;
