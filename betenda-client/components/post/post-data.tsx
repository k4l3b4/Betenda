import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Heart, Share2, MessageCircle } from "lucide-react"


const PostData = () => {
    return (
        <div className="w-[550px] p-2">
            <div>
                <div className="flex items-center gap-x-2" id="user">
                    <Avatar>
                        <AvatarImage src="https://github.com/shadcn.png" alt="@shadcn" />
                        <AvatarFallback>CN</AvatarFallback>
                    </Avatar>
                    <div className="flex items-baseline gap-x-2">
                        <div>
                            <p className="font-medium">Kaleb Abebe</p>
                            <p className="text-xs text-muted-foreground">@kalebቶ</p>
                        </div>
                        <span className="text-xs">•</span>
                        <p className="text-xs text-muted-foreground">2 hours ago</p>
                    </div>
                </div>
                <div className="p-2 text-sm" id="post">
                    U know i&apos;ve been thinking all of this shit is pure trash catch ma ballz..
                    U know i&apos;ve been thinking all of this shit is pure trash catch ma ballz..
                    U know i&apos;ve been thinking all of this shit is pure trash catch ma ballz..
                </div>
            </div>
            <section id="actions" className="flex flex-row justify-around">
                <div className="flex flex-row items-center text-center">
                    <Button variant={null} size="icon">
                        <Heart className="h-5 w-5" />
                    </Button>
                    <p className="text-xs font-medium">99K</p>
                </div>
                <div className="flex flex-row items-center text-center">
                    <Button variant={null} size="icon">
                        <MessageCircle className="h-5 w-5" />
                    </Button>
                    <p className="text-xs font-medium">13K</p>
                </div>
                <div>
                    <Button variant={null} size="icon">
                        <Share2 className="h-5 w-5" />
                    </Button>
                </div>
            </section>
        </div>
    );
}

export default PostData;