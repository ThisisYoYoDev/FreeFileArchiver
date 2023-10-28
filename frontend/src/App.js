import React from 'react';
import {
  ChakraProvider,
  Box,
  HStack,
  Grid,
  theme,
} from '@chakra-ui/react';
import FileUpload from './components/FileUpload';
import { useForm } from "react-hook-form";

function App() {
  const {
    control,
  } = useForm();

  const bodyStyles = {
    backgroundImage: `url('https://images.pexels.com/photos/1525041/pexels-photo-1525041.jpeg')`,
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
