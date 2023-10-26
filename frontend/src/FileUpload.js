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
  Progress
} from "@chakra-ui/react";
import { useController, useForm } from "react-hook-form";
import FileItem from "./FileItem";

export const FileUpload = ({ name, acceptedFileTypes, children, isRequired = false }) => {
  const inputRef = useRef();
  const [dragging, setDragging] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const { handleSubmit, control } = useForm();
  
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
    setSelectedFiles(updatedFiles);
  };

  const handleDownloadFile = (fileIndex) => {
    const file = selectedFiles[fileIndex];
    // Implémentez ici votre logique de téléchargement de fichier spécifique.
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
            {...useController({ name, control })}
            style={{ display: 'none' }}
          />

          <Stack spacing={4} align="center">
            <IconButton
              aria-label="Upload File"
              icon={<Image src="https://www.flaticon.com/free-icons/drag-and-drop" />}
              onClick={() => inputRef.current.click()}
              bg="transparent"
              _hover={{ bg: "transparent" }}
              height={500}
              width="100%"
            />
            <Text>Drag and drop files here or</Text>
          </Stack>
        </Box>
        <Box w="30%">
          <Stack spacing={4}>
            {selectedFiles.map((file, index) => (
              <FileItem
                key={index}
                file={file}
                onDelete={() => handleRemoveFile(index)}
                onDownload={() => handleDownloadFile(index)}
              />
            ))}
          </Stack>
        </Box>
      </Flex>
    </FormControl>
  );
};

FileUpload.defaultProps = {
  acceptedFileTypes: '',
};

export default FileUpload;
