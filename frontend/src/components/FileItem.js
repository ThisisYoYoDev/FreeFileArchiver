import React, { useState, useEffect } from "react";
import {
  Box,
  Text,
  Button,
  HStack,
  Progress,
  VStack,
} from "@chakra-ui/react";
import { FiDownload, FiTrash } from "react-icons/fi";
import { FaFilePdf, FaFileImage } from "react-icons/fa";

const FileItem = ({ file, onDelete, onDownload, uploadProgress }) => {
  const [progress, setProgress] = useState(0);
  const getFileIcon = (filename) => {
    const extension = filename.split(".").pop().toLowerCase();

    if (extension === "pdf") {
      return <FaFilePdf />;
    } else if (["jpg", "jpeg", "png", "gif"].includes(extension)) {
      return <FaFileImage />;
    } else {
      return null;
    }
  };


  useEffect(() => {
    const interval = setInterval(() => {
      if (progress < uploadProgress) {
        setProgress(progress + 1);
      }
    }, 10);

    return () => {
      clearInterval(interval);
    };
  }, [progress, uploadProgress]);

  return (
    <Box
      p={4}
      borderWidth="1px"
      borderRadius="lg"
      display="flex"
      flexDirection="column"
      alignItems="center" 
      justifyContent="space-between"
      backgroundColor="rgba(255, 255, 255, 0.9)"
      overflow="hidden"
    >
      <HStack spacing={2} align="center" w="100%">
        {getFileIcon(file.name)}
        <Box flex="1" overflow="hidden" whiteSpace="nowrap" textOverflow="ellipsis">
          <Text>{file.name}</Text>
        </Box>
        <HStack spacing={2}>
          <Button leftIcon={<FiDownload />} onClick={() => onDownload(file)} variant="ghost" size="sm" />
          <Button leftIcon={<FiTrash />} onClick={() => onDelete(file)} variant="ghost" color="red" size="sm" />
        </HStack>
      </HStack>
      <VStack spacing={2} w="100%">
        <Progress hasStripe value={progress} size="xs" w="100%" />
        <Text>{progress}%</Text>
      </VStack>
    </Box>
  );
};

export default FileItem;
