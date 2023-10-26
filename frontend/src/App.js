import React from 'react';
import {
  ChakraProvider,
  Box,
  Text,
  Link,
  HStack,
  Code,
  Grid,
  theme,
} from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import FileUpload from './FileUpload';
import { useForm } from "react-hook-form";

function App() {
  const {
    handleSubmit,
    register,
    setError,
    control,
    formState: { errors, isSubmitting },
  } = useForm();

  const bodyStyles = {
    backgroundImage: `url('https://images.pexels.com/photos/1525041/pexels-photo-1525041.jpeg')`, // Remplacez par le chemin de votre image
    backgroundSize: 'cover',
    backgroundAttachment: 'fixed',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    minHeight: '100vh',
  };

  return (
    <ChakraProvider theme={theme}>
      <div style={bodyStyles}>
        <Grid minH="70vh" p={20}>
          {/* <ColorModeSwitcher justifySelf="flex-end" p={10} /> */}
          <Box
            justifyContent={"center"}
            boxShadow='base'
            p='10'
            rounded='md'
            backgroundColor="rgba(255, 255, 255, 0.7)" 
            borderRadius={"10px"}
          >
            <HStack spacing={8}>
              <FileUpload name="avatar"
                acceptedFileTypes="*"
                isRequired={false}
                placeholder="Drop your files here or Browse."
                control={control}
              >
              </FileUpload>
            </HStack>
          </Box>
        </Grid>
      </div>
    </ChakraProvider>
  );
}

export default App;
