<?php

require 'vendor/autoload.php';
use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;

class HotlinePulling
{
    private $apiUrl = 'https://10.10.0.20:8443/recapi';
    private $apiUser = 'cdrapi';
    private $apiPwd = 'cdrapi123';
    private $storageDir = 'C:\\Users\\Luis M Leitao\\Documents\\new_cid\\hotline_api'; // Adjust as necessary
    private $apiPath = 'voicemail'; // API path for pulling files
    private $apiExtension = '5000'; // API extension, example value
    private $client = null;
    private $logFilePath = 'C:\\Users\\Luis M Leitao\\Documents\\new_cid\\hotline_api\\log.txt'; // Path to log file

    public function __construct()
    {
        $this->startPulling(); // Automatically start pulling and downloading.
    }

    public function startPulling()
    {
        try {
            $this->buildClient(); // Starts GuzzleHttp client
            $hotlines = $this->getHotlines();

            foreach ($hotlines as $hotline) {
                try {
                    $files = $this->getHotlineFiles($hotline);

                    foreach ($files as $file) {
                        $filenameWithExtension = sprintf('%s_%s', date('y'), $file['filename']);
                        $filename = sprintf('%s_%s', date('y'), pathinfo($file['filename'], PATHINFO_FILENAME));

                        $entityId = $hotline['filename'] . DIRECTORY_SEPARATOR . $filename;

                        $fileDownloadedPath = $this->downloadFiles(
                            $file['directory'], 
                            $file['filename'], 
                            $filenameWithExtension
                        );
                    }
                } catch (\Exception $e) {
                    $this->createLog("Error processing hotline {$hotline['filename']}: " . $e->getMessage());
                }
            }
        } catch (\Exception $e) {
            $this->createLog("Error starting hotline pulling: " . $e->getMessage());
        }
    }

    private function buildClient()
    {
        $this->client = new Client([
            'base_uri' => $this->apiUrl,
            'verify' => false,
        ]);
        $this->createLog('Build Client');
    }

    private function createLog($message)
    {
        $logMessage = "[" . date('Y-m-d H:i:s') . "] " . $message . "\n";
        file_put_contents($this->logFilePath, $logMessage, FILE_APPEND);
    }

    protected function get(array $query = [], array $options = [])
    {
        try {
            $opts = array_merge([
                \GuzzleHttp\RequestOptions::VERIFY => false,
                \GuzzleHttp\RequestOptions::AUTH => [$this->apiUser, $this->apiPwd, 'digest'],
                \GuzzleHttp\RequestOptions::QUERY => $query,
            ], $options);

            return $this->client->get('', $opts);
        } catch (RequestException $e) {
            $this->createLog("GET request failed: " . $e->getMessage());
            throw $e;
        }
    }

    protected function getHotlines(): array
    {
        $this->createLog('Get Hotlines Extensions');

        $response = $this->get(["filedir" => $this->apiPath]);
        $content = $response->getBody()->getContents();
        $allExtensions = $this->formatResponseBodyContents($content);

        $this->createLog('Found Extensions: ' . print_r($allExtensions, true));

        $extensions = [];
        if (!empty($this->apiExtension)) {
            $filterExtensions = array_map('trim', explode(',', $this->apiExtension));

            $this->createLog('Filtering extensions by: ' . print_r($filterExtensions, true));
            
            foreach ($allExtensions as $extension) {
                $filename = trim(strtolower($extension['filename']));
                if (in_array($filename, $filterExtensions)) {
                    $extensions[] = $extension;
                }
            }
        } else {
            $extensions = $allExtensions;
        }

        $this->createLog('Extensions to be processed: ' . print_r($extensions, true));

        return $extensions;
    }

    protected function getHotlineFiles(array $arrayFile)
    {
        $fileDir = sprintf('%s/default/%s/INBOX', $this->apiPath, $arrayFile['filename']);

        $response = $this->get(["filedir" => $fileDir]);
        $content = $response->getBody()->getContents();
        $this->createLog('Get Hotlines Files: ' . print_r($content, true));
        return $this->formatResponseBodyContents($content);
    }

    protected function formatResponseBodyContents($content): array
    {
        $csv = explode("\n", $content);
        array_shift($csv); // Assuming first line is headers, remove if not needed
    
        $formattedArray = array_map(function ($item) {
            $parts = explode(',', $item);
            // Ensure that there's a part[1] before attempting to use it
            return [
                'filename' => $parts[1] ?? 'default_filename', // Provide a default or handle the absence as necessary
                'directory' => $parts[0]
            ];
        }, $csv);
    
        return $formattedArray;
    }
    

    protected function downloadFiles(string $directory, string $filename, string $diskName)
    {
        $query = [
            'filedir' => $directory,
            'filename' => $filename,
        ];

        $storageDir = $this->getStorageDir();
        $dirPath = $storageDir . DIRECTORY_SEPARATOR . $directory;

        if (!is_dir($dirPath) && !mkdir($dirPath, 0755, true) && !is_dir($dirPath)) {
            $this->createLog("Error creating folder: $dirPath");
            throw new \RuntimeException(sprintf('Directory "%s" was not created', $dirPath));
        }

        $filePath = $dirPath . DIRECTORY_SEPARATOR . $diskName;
        $fileStream = fopen($filePath, 'w');
        if (!$fileStream) {
            $this->createLog("Error opening file: $filePath");
            throw new \RuntimeException("Cannot open file: $filePath");
        }

        try {
            $this->get($query, [\GuzzleHttp\RequestOptions::SINK => $fileStream]);
        } catch (\Exception $e) {
            $this->createLog("Failed to download file: $filePath. Error: " . $e->getMessage());
            throw $e;
        } finally {
            if (is_resource($fileStream)) {
                fclose($fileStream);
            }
        }

        $this->createLog("Downloaded file: $filePath");

        return $filePath;
    }

    protected function getStorageDir()
    {
        $folder = rtrim($this->storageDir, '\\');
        if (!is_dir($folder)) {
            if (!mkdir($folder, 0755, true) && !is_dir($folder)) {
                $this->createLog(sprintf('Error creating directory "%s"', $folder));
                throw new \RuntimeException(sprintf('Directory "%s" was not created', $folder));
            }
        }
        return $folder;
    }
}

// Instantiate the class to start pulling process
$downloader = new HotlinePulling();

