import React from 'react';
import { PropTypes } from 'prop-types';
import { FilePond, registerPlugin } from 'react-filepond';
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type';
import 'filepond/dist/filepond.min.css';
import './index.css';

registerPlugin(FilePondPluginFileValidateType);

export default function FileUploader({ files, onFileUpdate }) {
  return (
    <>
      <FilePond
        files={files}
        required
        acceptedFileTypes={[
          // can only upload .csv file
          'text/csv',
          'text/plain'
          // 'application/vnd.ms-excel',
          // 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        ]}
        fileValidateTypeDetectType={(source, type) =>
          // Note: we need this here to activate the file type validations and filtering
          new Promise((resolve, reject) => {
            // Do custom type detection here and return with promise
            resolve(type);
          })
        }
        allowFileEncode
        onupdatefiles={onFileUpdate}
        name="files"
        labelIdle='Drag your file here or <span class="filepond--label-action">Browse</span>'
      />
    </>
  );
}

FileUploader.propTypes = {
  files: PropTypes.array.isRequired,
  onFileUpdate: PropTypes.func.isRequired,
};
