import React, { useState, useRef } from "react";
import {
  Box,
  FormControl,
  FormLabel,
  Stack,
  IconButton,
  Text,
  Flex,
  Image,
  Button
} from "@chakra-ui/react";
import FileItem from "./FileItem";
import axios from "axios";

export const FileUpload = ({ name, acceptedFileTypes, children, isRequired = false }) => {
  const inputRef = useRef();
  const [dragging, setDragging] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploadProgress, setUploadProgress] = useState([]);

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    if (droppedFiles.length > 0) {
      setSelectedFiles([...selectedFiles, ...droppedFiles]);
    }
  };

  const handleFileInputChange = (e) => {
    const selectedInputFiles = Array.from(e.target.files);
    setSelectedFiles([...selectedFiles, ...selectedInputFiles]);
  };

  const handleRemoveFile = (fileIndex) => {
    const updatedFiles = [...selectedFiles];
    updatedFiles.splice(fileIndex, 1);

    const updatedProgress = [...uploadProgress];
    updatedProgress.splice(fileIndex, 1);

    setSelectedFiles(updatedFiles);
    setUploadProgress(updatedProgress);
  };

  const handleDownloadFile = async (id) => {
    if (id !== null) {
      const downloadUrl = `http://127.0.0.1:8000/download/${id}`;
      await navigator.clipboard.writeText(downloadUrl);
    }
  };

  const submitUpload = async () => {
    const uploadPromises = selectedFiles.map(async (file, index) => {
      if (uploadProgress[index]?.progress === 100) {
        return;
      }
      const formData = new FormData();
      formData.append("file", file);

      console.log(`Uploading file: ${file.name}`);

      const headers = {
        "Content-Disposition": `attachment; filename="${file.name}"`,
      };

      const config = {
        onUploadProgress: function (progressEvent) {
          const percentCompleted = Math.round((progressEvent.loaded / progressEvent.total) * 100);
          
          setUploadProgress((prevProgress) => {
            const updatedProgress = [...prevProgress];
            const index = selectedFiles.indexOf(file);
            updatedProgress[index] = { id: null, progress: percentCompleted };
            return updatedProgress;
          });
        },
        headers,
      };

      try {
        const response = await axios.post("http://127.0.0.1:8000/upload", formData, config);
        console.log(`File ${file.name} uploaded successfully. Response:`, response);

        const id = response.data.id;
        setUploadProgress((prevProgress) => {
          const updatedProgress = [...prevProgress];
          const index = selectedFiles.indexOf(file);
          updatedProgress[index] = { id, progress: 100 };
          return updatedProgress;
        });
      } catch (error) {
        console.error(`Error uploading file ${file.name}:`, error);
      }
    });

    await Promise.all(uploadPromises);
  };

  return (
    <FormControl>
      <FormLabel htmlFor="writeUpFile">{children}</FormLabel>
      <Flex placeContent={"center"}>
        <Box
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          w="30%"
          minH="400px"
          mr={4}
          p={4}
          border={`3px dashed ${dragging ? 'blue' : 'gray'}`}
          borderRadius="10px"
          cursor="pointer"
          backgroundColor="rgba(255, 255, 255, 0.8)"
        >
          <input
            type="file"
            onChange={handleFileInputChange}
            accept={acceptedFileTypes}
            name={name}
            ref={inputRef}
            multiple
            style={{ display: 'none' }}
          />

          <Stack spacing={4} align="center">
            <IconButton
              aria-label="Upload File"
              icon={<Image w={100} src="https://www.freeiconspng.com/uploads/document-icon-19.png" />}
              onClick={() => inputRef.current.click()}
              bg="transparent"
              _hover={{ bg: "transparent" }}
              height={500}
              width="100%"
            />
            <Text>Drag and drop files here or Browse files</Text>
          </Stack>
        </Box>
        <Box w="30%">
          <Stack spacing={4}>
            {selectedFiles.map((file, index) => (
              <FileItem
                key={index}
                file={file}
                onDelete={() => handleRemoveFile(index)}
                onDownload={() => handleDownloadFile(uploadProgress[index]?.id)}
                uploadProgress={uploadProgress[index]?.progress}
              />
            ))}
          </Stack>
        </Box>
      </Flex>
      <Flex justifyContent="center" p={5}>
        <Button onClick={submitUpload}>Submit upload</Button>
      </Flex>
    </FormControl>
  );
};

export default FileUpload;
