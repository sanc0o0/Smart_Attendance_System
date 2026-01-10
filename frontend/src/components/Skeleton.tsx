export default function Skeleton({
    height = "h-6",
    width = "w-full",
}: {
    height?: string;
    width?: string;
}) {
    return (
        <div
            className={`animate-pulse bg-gray-200 rounded ${height} ${width}`}
        />
    );
}
