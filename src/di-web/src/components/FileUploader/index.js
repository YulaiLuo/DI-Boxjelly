import React from 'react';
import { FilePond, registerPlugin } from 'react-filepond';
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type';
import 'filepond/dist/filepond.min.css';
import './index.css';

registerPlugin(FilePondPluginFileValidateType);

export default function FileUploader({files, onFileUpdate}) {
  
  return (
    <>
      <FilePond
        files={files}
        required
        acceptedFileTypes={[ // can only upload .csv, .xls, and .xlsx file
          'text/csv',
          'application/vnd.ms-excel',
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
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
