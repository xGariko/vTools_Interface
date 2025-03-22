export const formatFileSize = (fileSizeInBytes: number): string => {
	const i = Math.floor(Math.log(fileSizeInBytes) / Math.log(1024));
	return (
		(fileSizeInBytes / Math.pow(1024, i)).toFixed(2) + ' ' + ['B', 'KB', 'MB', 'GB', 'TB'][i]
	);
};
