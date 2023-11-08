import React, { useState, useRef } from 'react';
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
import { useToast } from '@chakra-ui/react'

export const FileUpload = ({ name, acceptedFileTypes, children, isRequired = false }) => {
  const inputRef = useRef();
  const [dragging, setDragging] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploadProgress, setUploadProgress] = useState([]);
  const requests = useRef([]);
  const toast = useToast()

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
      setUploadProgress([...uploadProgress, { id: null, progress: 0 }]);
    }
  };

  const handleFileInputChange = (e) => {
    const selectedInputFiles = Array.from(e.target.files);
    setSelectedFiles([...selectedFiles, ...selectedInputFiles]);
    setUploadProgress([...uploadProgress, { id: null, progress: 0 }]);
  };

  const handleRemoveFile = (fileIndex) => {
    const updatedFiles = [...selectedFiles];
    updatedFiles.splice(fileIndex, 1);

    const updatedProgress = [...uploadProgress];
    updatedProgress.splice(fileIndex, 1);

    setSelectedFiles(updatedFiles);
    setUploadProgress(updatedProgress);

    const request = requests.current[fileIndex];
    if (request) {
      request.cancel("Upload canceled");
      toast({
        title: `File ${selectedFiles[fileIndex].name} removed!`,
        status: 'success',
        isClosable: true,
        position: 'top'
      })
    }
  };

  const handleDownloadFile = async (id) => {
    if (id !== null) {
      const downloadUrl = `http://127.0.0.1:8000/download/${id}`;
      window.open(downloadUrl, "_blank");
    }
  };

  const handleShareLink = async (id) => {
    if (navigator.share) {
      try {
        await navigator.share({ url: `http://127.0.0.1:8000/download/${id}` });
      } catch (error) {
        toast({
          title: `Error sharing link`,
          status: 'error',
          isClosable: true,
          position: 'top'
        })
      }
    } else {
      toast({
        title: `Link copied to clipboard`,
        status: 'success',
        isClosable: true,
        position: 'top'
      })
      await navigator.clipboard.writeText(`http://127.0.0.1:8000/download/${id}`);
    }
  };

  const submitUpload = async () => {
    requests.current = [];

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
            updatedProgress[index] = { id: null, progress: percentCompleted };
            return updatedProgress;
          });
        },
        headers,
      };

      try {
        const source = axios.CancelToken.source();
        const request = await axios.post("http://127.0.0.1:8000/upload", formData, {
          ...config,
          cancelToken: source.token,
        });

        requests.current[index] = source;

        const response = request;
        const id = response.data.id;
        toast({
          title: `File ${file.name} uploaded!`,
          status: 'success',
          isClosable: true,
          position: 'top'
        })
        setUploadProgress((prevProgress) => {
          const updatedProgress = [...prevProgress];
          updatedProgress[index] = { id, progress: 100 };
          return updatedProgress;
        });
      } catch (error) {
        if (!axios.isCancel(error)) {
          console.error(`Error uploading file ${file.name}:`, error);
        }
      }
    });

    try {
      await Promise.all(uploadPromises);
    } catch (error) {
      console.error("One or more uploads failed:", error);
    }
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
                onDownload={() => handleDownloadFile(uploadProgress[index]?.id)}
                onShare={() => handleShareLink(uploadProgress[index]?.id)}
                onCancel={() => handleRemoveFile(index)}
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
